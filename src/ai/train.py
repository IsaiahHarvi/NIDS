import os
import click
import wandb
import torch
import lightning.pytorch as pl
from lightning.pytorch.loggers import WandbLogger
from lightning.pytorch.callbacks import ModelCheckpoint, EarlyStopping
from torch.nn import CrossEntropyLoss, MSELoss
from icecream import ic
from dvclive.lightning import DVCLiveLogger

from ai.DataModule import DataModule
from ai.BasicModule import BasicModule, ResidualNetwork, Autoencoder
from ai.transforms import MinMaxTransform

@click.command()
@click.option("--epochs", default=1000)
@click.option("--batch_size", default=256)  # >=256 when all_data
@click.option("--target_batch", default=256)  # used for gradient accumulation
@click.option("--lr", default=0.001)
@click.option("--early_stop_patience", default=10)
@click.option(
    "--constructor",
    type=click.Choice(["ResidualNetwork"], case_sensitive=False),
    prompt=True,
)
@click.option("--all_data", is_flag=True, default=False)
def main(epochs, batch_size, target_batch, constructor, all_data, lr, early_stop_patience):
    torch.set_float32_matmul_precision("medium")
    if target_batch < batch_size:
        target_batch = batch_size

    if all_data:
        paths = [
            f"data/CIC/{csv}" for csv in os.listdir("data/CIC") if csv.endswith(".csv") and "test_data" not in csv
        ]
    else:
        paths = [
            "data/CIC/Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv",
            "data/CIC/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv",
            "data/CIC/Friday-WorkingHours-Morning.pcap_ISCX.csv",
            "data/CIC/Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv",
        ]

    constructor = {"ResidualNetwork": ResidualNetwork}[constructor]

    train(epochs, batch_size, target_batch, paths, constructor, lr, early_stop_patience)

def train(epochs, batch_size, target_batch, paths, constructor, lr, early_stop_patience):
    dm = DataModule(
        paths=paths,
        val_split=0.1,
        batch_size=batch_size, 
        num_workers=os.cpu_count(),
        transform=MinMaxTransform(),
    )
    dm.setup()
    ic(dm.n_classes)
    ic(dm.example_shape)
    model = BasicModule(
        model_constructor=constructor,
        in_features=dm.example_shape,
        hidden_size=128, 
        out_features=dm.n_classes,
        lr=lr,
        class_weights=dm.class_weights,
        criterion=MSELoss if isinstance(constructor, Autoencoder) else CrossEntropyLoss,
        model_constructor_kwargs={
            "num_layers": 2,
        }
    )

    ckpt = ModelCheckpoint(
        dirpath="data/checkpoints",
        filename=f"{model.constructor.__class__.__name__}",
        save_top_k=1,
        every_n_epochs=1,
    )

    early_stop = EarlyStopping(
        monitor="val_loss",
        patience=early_stop_patience,
        verbose=False,
        mode="min"
    )

    wandb.init(
        project="NIDS",
        config={
            # "epochs": epochs, # early stopping makes this useless
            "batch_size": batch_size,
            # "target_batch": target_batch, # we arent acumulating batches anymore
            "learning_rate": lr,
            "early_stop_patience": early_stop_patience,
            "model_constructor": constructor.__name__,
            "model_constructor_kwargs": model.constructor_kwargs,
        },
        group="DDP"
    )
    wandb.require("core")

    trainer = pl.Trainer(
        max_epochs=epochs,
        logger=[DVCLiveLogger(), WandbLogger()],
        # accumulate_grad_batches=(max(1, target_batch // batch_size)),
        callbacks=[ckpt, early_stop],
        accelerator="gpu",
        devices="auto",
    )

    trainer.fit(model, dm.train_dataloader(), dm.val_dataloader())
    trainer.save_checkpoint(
        f"data/checkpoints/{model.constructor.__class__.__name__}.ckpt"
    )
    trainer.test(model, dm.val_dataloader(shuffle=True))
    wandb.finish()

if __name__ == "__main__":
    main()
