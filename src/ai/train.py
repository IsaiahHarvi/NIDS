import os
import lightning.pytorch as pl
import click
from icecream import ic
from dvclive.lightning import DVCLiveLogger

from data.CIC.check_data import collect_data
from ai.DataModule import DataModule
from ai.BasicModule import BasicModule, RNN

@click.command()
@click.option("--epochs", default=10)
@click.option("--batch_size", default=64)
@click.option("--target_batch", default=64)
@click.option("--all_data", is_flag=True, default=False)
def main(epochs, batch_size, target_batch, all_data):
    train(epochs, batch_size, target_batch, all_data)
    
def train(epochs, batch_size, target_batch, all_data):
    dm = DataModule(
        paths=[
            f"data/CIC/Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv",
            f"data/CIC/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"   
        ] if not all_data else collect_data(),
        batch_size=batch_size, 
        val_split=0.2
    )
    dm.setup()
    ic(dm.n_classes)

    model = BasicModule(
        model_constructor=RNN,
        in_features=dm.train_dataset[0][0].shape[1], # not strictly necessary as a param, but its nice metadata
        hidden_size=128, 
        out_features=dm.n_classes,
        lr=0.001,
        accumulate_grad_batches=(max(1, target_batch // dm.batch_size)),
        batch_size=dm.batch_size # used for model_constructors
    )
    
    trainer = pl.Trainer(
        max_epochs=epochs, 
        logger=DVCLiveLogger()
    )

    trainer.fit(model, dm.train_dataloader(), dm.val_dataloader())
    trainer.save_checkpoint(f"data/checkpoints/{model.__class__.__name__}.ckpt")
    trainer.test(model, dm.val_dataloader(shuffle=True))


if __name__ == "__main__":
    main()
