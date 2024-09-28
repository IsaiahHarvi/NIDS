import os
import torch
import numpy as np
import lightning.pytorch as pl
import pandas as pd
from torch.utils.data import DataLoader, Dataset, Subset
from sklearn.utils.class_weight import compute_class_weight
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import StandardScaler
from icecream import ic

class CIC_IDS(Dataset):
    def __init__(self, data, labels, transform=None):
        self.data = data
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        x = self.data[idx]
        y = self.labels[idx]

        if self.transform:
            x = self.transform(x)

        return torch.tensor(x, dtype=torch.float32), torch.tensor(y, dtype=torch.long)


class DataModule(pl.LightningDataModule):
    def __init__(
        self,
        paths: list[str],
        batch_size: int = 64,
        val_split: float = 0.2,
        num_workers: int = os.cpu_count(),
    ):
        super().__init__()
        self.paths = paths
        self.batch_size = batch_size
        self.val_split = val_split
        self.n_classes = 0
        self.num_workers = num_workers
        self.scaler = StandardScaler()  # For Z-score standardization

    def setup(self):
        dfs: list[pd.DataFrame] = []
        for path in self.paths:
            df: pd.DataFrame = pd.read_csv(path)
            df.columns = df.columns.str.strip().str.replace(" ", "_")
            dfs.append(df)

        df = pd.concat(dfs, ignore_index=True)

        drop_columns = [
            'Flow_ID', 'Source_IP', 'Destination_IP', 'Timestamp',  # Redundant features
            'Bwd_PSH_Flags', 'Bwd_URG_Flags', 'Fwd_Avg_Bytes/Bulk', 'Fwd_Avg_Packets/Bulk',
            'Fwd_Avg_Bulk_Rate', 'Bwd_Avg_Bytes/Bulk', 'Bwd_Avg_Packets/Bulk', 'Bwd_Avg_Bulk_Rate'
        ]

        df = df.drop(drop_columns, axis=1, errors="ignore")
        df = df.replace([np.inf, -np.inf], np.nan).dropna()

        x = df.select_dtypes(include=[float, int])
        y = df["Label"].astype("category").cat.codes

        class_labels = df["Label"].values
        unique_labels = df["Label"].unique()
        label_mapping = {label: idx for idx, label in enumerate(unique_labels)}
        ic(label_mapping)

        class_indices = [label_mapping[label] for label in class_labels]

        class_weights = compute_class_weight(
            "balanced", classes=np.unique(class_indices), y=class_indices
        )
        self.class_weights = torch.tensor(class_weights, dtype=torch.float32)

        self.n_classes = len(np.unique(y))
        self.example_shape = x.shape[1]

        x = self.scaler.fit_transform(x)

        dataset = CIC_IDS(x, y.values)
        shuffle_split = StratifiedShuffleSplit(n_splits=1, test_size=self.val_split)
        train_idx, val_idx = next(shuffle_split.split(x, y))

        self.train_dataset = Subset(dataset, train_idx)
        self.val_dataset = Subset(dataset, val_idx)

    def train_dataloader(self):
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=self.num_workers,
        )

    def val_dataloader(self, shuffle: bool = False):
        return DataLoader(
            self.val_dataset,
            batch_size=self.batch_size,
            shuffle=shuffle,
            num_workers=self.num_workers,
        )
