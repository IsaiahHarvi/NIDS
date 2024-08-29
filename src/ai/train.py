import os
import wandb
import click
import lightning.pytorch as pl
from lightning.pytorch.loggers import WandbLogger
from lightning.pytorch.callbacks import ModelCheckpoint, EarlyStopping
from icecream import ic
from dvclive.lightning import DVCLiveLogger

from ai.DataModule import DataModule
from ai.BasicModule import BasicModule, RNN, ResidualNetwork

@click.command()
@click.option("--epochs", default=1000)
@click.option("--batch_size", default=64)  # >=256 when all_data
@click.option("--target_batch", default=64)  # used for gradient accumulation
@click.option(
    "--constructor",
    type=click.Choice(["ResidualNetwork"], case_sensitive=False),
    prompt=True,
)
@click.option("--all_data", is_flag=True, default=False)
def main(epochs, batch_size, target_batch, constructor, all_data):
    if target_batch < batch_size:
        target_batch = batch_size

    if all_data:
        paths = [
            f"data/CIC/{csv}" for csv in os.listdir("data/CIC") if csv.endswith(".csv")
        ]
    else:
        paths = [
            "data/CIC/Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv",
            "data/CIC/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv",
            # "data/CIC/Friday-WorkingHours-Morning.pcap_ISCX.csv",
        ]

    constructor = {"ResidualNetwork": ResidualNetwork}[constructor]

    train(epochs, batch_size, target_batch, paths, constructor)

def train(epochs, batch_size, target_batch, paths, constructor):
    dm = DataModule(
        paths=paths,
        val_split=0.2,
        batch_size=batch_size, 
        num_workers=os.cpu_count()
    )
    dm.setup()
    ic(dm.n_classes)

    model = BasicModule(
        model_constructor=constructor,
        in_features=dm.train_dataset[0][0].shape[1], # this param is not strictly necessary, but its nice metadata
        hidden_size=128, 
        out_features=dm.n_classes,
        lr=0.001,
        model_constructor_kwargs={
            "num_blocks": 3,  # used for ResidualNetwork
        },
    )

    ckpt = ModelCheckpoint(
        dirpath="data/checkpoints",
        filename=f"{model.constructor.__class__.__name__}",
        save_top_k=1,
        every_n_epochs=1,
    )

    early_stop = EarlyStopping(
        monitor='val_loss',
        patience=10,
        verbose=True,
        mode='min' 
    )

    wandb.init(
        project="NIDS",
        config={
            "epochs": epochs,
            "batch_size": batch_size
        }
    )

    trainer = pl.Trainer(
        max_epochs=epochs,
        logger=[DVCLiveLogger(), WandbLogger()],
        accumulate_grad_batches=(max(1, target_batch // batch_size)),
        callbacks=[ckpt, early_stop],
        # accelerator="gpu" if torch.cuda.is_available() else "cpu",
        # devices=torch.cuda.device_count() if torch.cuda.is_available() else os.cpu_count()
    )

    trainer.fit(model, dm.train_dataloader(), dm.val_dataloader())
    trainer.save_checkpoint(
        f"data/checkpoints/{model.constructor.__class__.__name__}.ckpt"
    )
    trainer.test(model, dm.val_dataloader(shuffle=True))
    wandb.finish()

if __name__ == "__main__":
    main()
