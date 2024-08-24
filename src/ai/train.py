import os
import torch
import lightning.pytorch as pl
import click
from icecream import ic
from dvclive.lightning import DVCLiveLogger

from ai.DataModule import DataModule
from ai.BasicModule import BasicModule, RNN

@click.command()
@click.option("--epochs", default=10)
@click.option("--batch_size", default=64)
@click.option("--target_batch", default=64)
@click.option("--all_data", is_flag=True, default=False)
def main(epochs, batch_size, target_batch, all_data):
    if all_data:
        paths = [f"data/CIC/{csv}" for csv in os.listdir("data/CIC") if csv.endswith('.csv')]
    else:
        paths=[
            f"data/CIC/Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv",
            f"data/CIC/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"   
        ]

    train(epochs, batch_size, target_batch, paths)
    
def train(epochs, batch_size, target_batch, paths):
    dm = DataModule(
        paths=paths,
        val_split=0.2,
        batch_size=batch_size, 
        num_workers=os.cpu_count()
    )
    dm.setup()
    ic(dm.n_classes)

    model = BasicModule(
        model_constructor=RNN,
        in_features=dm.train_dataset[0][0].shape[1], # this param is not strictly necessary, but its nice metadata
        hidden_size=128, 
        out_features=dm.n_classes,
        lr=0.001,
        batch_size=dm.batch_size # used for model_constructors
    )
    
    trainer = pl.Trainer(
        max_epochs=epochs, 
        logger=DVCLiveLogger(),
        accumulate_grad_batches=(max(1, target_batch // batch_size)),
        accelerator="gpu" if torch.cuda.is_available() else "cpu",
        devices=torch.cuda.device_count() if torch.cuda.is_available() else os.cpu_count()
    )

    trainer.fit(model, dm.train_dataloader(), dm.val_dataloader())
    trainer.save_checkpoint(f"data/checkpoints/{model.__class__.__name__}.ckpt")
    trainer.test(model, dm.val_dataloader(shuffle=True))


if __name__ == "__main__":
    main()
