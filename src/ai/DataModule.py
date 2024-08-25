import os
import torch
import numpy as np
import lightning.pytorch as pl
import pandas as pd
from torch.utils.data import DataLoader, TensorDataset, random_split
from sklearn.preprocessing import StandardScaler
from icecream import ic

class DataModule(pl.LightningDataModule):
    def __init__(self, paths: list[str], batch_size: int =64, val_split: float=0.2, num_workers: int=os.cpu_count()):
        super().__init__()
        self.paths = paths
        self.batch_size = batch_size
        self.val_split = val_split
        self.n_classes = 0
        self.num_workers = num_workers

    def setup(self):
        dfs = []
        for path in self.paths:
            df = pd.read_csv(path)
            df.columns = df.columns.str.strip().str.replace(' ', '_')
            dfs.append(df)

        df = pd.concat(dfs, ignore_index=True)
        df = df.drop(["Flow_ID", "Source_IP", "Destination_IP", "Timestamp"], axis=1, errors="ignore")
        # ic(df) 
        x = df.select_dtypes(include=[float, int]).fillna(0)
        x.replace([np.inf, -np.inf], np.nan, inplace=True)
        x.fillna(x.mean(), inplace=True)

        y = df["Label"].astype("category").cat.codes
        ic(df["Label"].unique())
        self.n_classes = len(y.unique())

        scaler = StandardScaler()
        x = scaler.fit_transform(x)
        
        x_tensor = torch.tensor(x, dtype=torch.float32)
        y_tensor = torch.tensor(y.values, dtype=torch.long)
        
        dataset = TensorDataset(x_tensor.unsqueeze(1), y_tensor)
        train_size = int((1 - self.val_split) * len(dataset))
        val_size = len(dataset) - train_size
        
        self.train_dataset, self.val_dataset = random_split(dataset, [train_size, val_size])

    def train_dataloader(self):
        return DataLoader(
            self.train_dataset, 
            batch_size=self.batch_size, 
            shuffle=True,
            num_workers=self.num_workers
        )

    def val_dataloader(self, shuffle: bool = False):
        return DataLoader(
            self.val_dataset, 
            batch_size=self.batch_size,
            shuffle=shuffle,
            num_workers=self.num_workers
        )
