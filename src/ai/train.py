import os
import lightning.pytorch as pl
import click
from dvclive.lightning import DVCLiveLogger

from ai.DataModule import DataModule
from ai.BasicModule import Recurrent

@click.command()
@click.option("--epochs", default=10)
def main(epochs):
    train(epochs)
    
def train(epochs):
    cic_dir = "data/CIC"
    all_csvs = os.listdir(cic_dir)
    dm = DataModule(
        # paths=[
        #     f"{cic_dir}/Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv",
        #     f"{cic_dir}/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"   
        # ],
        paths = all_csvs,
        batch_size=64, 
        test_size=0.2
    )
    dm.prepare_data()

    model = Recurrent(
        in_features=dm.train_dataset[0][0].shape[1],
        hidden_size=128, 
        out_features=dm.n_classes,
        lr=0.001
    )
    
    trainer = pl.Trainer(
        max_epochs=epochs, 
        logger=DVCLiveLogger()
    )

    trainer.fit(model, dm.train_dataloader(), dm.val_dataloader())
    trainer.save_checkpoint(f"data/checkpoints/{model.__class__.__name__}.ckpt")
    trainer.test(model, dm.val_dataloader())

if __name__ == "__main__":
    main()
