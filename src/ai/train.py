import os
import click
import wandb
import torch
import lightning.pytorch as pl
from lightning.pytorch.loggers import WandbLogger
from lightning.pytorch.callbacks import ModelCheckpoint, EarlyStopping
from torch.nn import CrossEntropyLoss
from icecream import ic
from dvclive.lightning import DVCLiveLogger

from ai.DataModule import DataModule
from ai.BasicModule import BasicModule, ResidualNetwork, MLP


@click.command()
@click.option("--epochs", default=1000)
@click.option("--batch_size", default=32)
@click.option("--lr", default=0.001)
@click.option("--early_stop_patience", default=10)
@click.option("--ckpt_name", default="best")
@click.option(
    "--constructor",
    type=click.Choice(["ResidualNetwork", "MLP"], case_sensitive=False),
    prompt=True,
)
@click.option("--all_data", is_flag=True, default=False)
def main(epochs, batch_size, constructor, all_data, lr, early_stop_patience, ckpt_name):
    torch.set_float32_matmul_precision("medium")

    if all_data:
        paths = [
            f"data/CIC/{csv}" for csv in os.listdir("data/CIC") if csv.endswith(".csv") and "test_data" not in csv
        ]
    else:
        paths = [
            "data/CIC/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv",
            "data/CIC/Friday-WorkingHours-Morning.pcap_ISCX.csv",
        ]

    constructor = {"ResidualNetwork": ResidualNetwork, "MLP" : MLP}[constructor]

    train(epochs, batch_size, paths, constructor, lr, early_stop_patience, ckpt_name)

def train(epochs, batch_size, paths, constructor, lr, early_stop_patience, ckpt_name):
    dm = DataModule(
        paths=paths,
        val_split=0.3,
        batch_size=batch_size, 
        num_workers=(os.cpu_count() // 2),
        # transform=MinMaxTransform(),
    )
    dm.setup()
    ic(dm.n_classes)
    ic(dm.example_shape)
    model = BasicModule(
        model_constructor=constructor,
        in_features=dm.example_shape,
        hidden_size=256, 
        out_features=dm.n_classes,
        lr=lr,
        class_weights=dm.class_weights,
        criterion=CrossEntropyLoss,
        # model_constructor_kwargs={
        #     "num_layers": 2,
        # }
    )

    ckpt = ModelCheckpoint(
        dirpath="data/checkpoints",
        filename=ckpt_name,
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
            "learning_rate": lr,
            "early_stop_patience": early_stop_patience,
            "model_constructor": constructor.__name__,
            "model_constructor_kwargs": model.constructor_kwargs,
            "ckpt_name": ckpt_name,
        },
        group="DDP" if torch.cuda.device_count() > 1 else "Single",
    )
    wandb.require("core")

    trainer = pl.Trainer(
        max_epochs=epochs,
        logger=[DVCLiveLogger(), WandbLogger()],
        callbacks=[ckpt, early_stop],
        accelerator="gpu" if torch.cuda.is_available() else "cpu",
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
