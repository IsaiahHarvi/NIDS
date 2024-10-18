import os
from collections import Counter

import lightning.pytorch as pl
import numpy as np
import pandas as pd
import torch
from icecream import ic
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.utils.class_weight import compute_class_weight
from torch.utils.data import DataLoader, Dataset, Subset


class CIC_IDS(Dataset):
    def __init__(self, data, labels, transform=None) -> None:
        self.data = data
        self.labels = labels
        self.transform = transform

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor]:
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
        num_workers: int = (os.cpu_count() // 2),
    ):
        super().__init__()
        self.paths = paths
        self.batch_size = batch_size
        self.val_split = val_split
        self.num_workers = num_workers
        self.scaler = StandardScaler()

    def setup(self) -> None:
        dfs: list[pd.DataFrame] = []
        for path in self.paths:
            df: pd.DataFrame = pd.read_csv(path)
            df.columns = df.columns.str.strip().str.replace(" ", "_")
            dfs.append(df)

        df = pd.concat(dfs, ignore_index=True)

        drop_columns = [
            "Flow_ID",
            "Timestamp",
            "Bwd_Avg_Packets/Bulk",
            "Bwd_Avg_Bulk_Rate",
            "Bwd_PSH_Flags",
            "Bwd_URG_Flags",
            "Fwd_Avg_Bytes/Bulk",
            "Fwd_Avg_Packets/Bulk",
            "Fwd_Avg_Bulk_Rate",
            "Bwd_Avg_Bytes/Bulk",
            "Fwd_Header_Length.1",
        ]
        df.drop(drop_columns, axis=1, errors="ignore", inplace=True)

        # Save pre-normalized metadata
        self.metadata = df.copy()

        df.drop(["Source_IP", "Destination_IP"], axis=1, errors="ignore", inplace=True)

        df = df.replace([np.inf, -np.inf], np.nan).dropna()
        x = df.select_dtypes(include=[float, int])

        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(df["Label"])

        class_weights = compute_class_weight("balanced", classes=np.unique(y), y=y)
        self.class_weights = torch.tensor(class_weights, dtype=torch.float32)

        self.n_classes = len(np.unique(y))
        self.example_shape = x.shape[1]

        x = self.scaler.fit_transform(x)

        dataset = CIC_IDS(x, y)
        shuffle_split = StratifiedShuffleSplit(n_splits=1, test_size=self.val_split)
        train_idx, val_idx = next(shuffle_split.split(x, y))

        self.train_dataset = Subset(dataset, train_idx)
        self.val_dataset = Subset(dataset, val_idx)

        # Store indices for the validation set to retrieve metadata later
        self.val_idx = val_idx

    def train_dataloader(self) -> DataLoader:
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=self.num_workers,
        )

    def val_dataloader(self, shuffle: bool = False) -> DataLoader:
        return DataLoader(
            self.val_dataset,
            batch_size=self.batch_size,
            shuffle=shuffle,
            num_workers=self.num_workers,
        )

    def get_metadata(self, idx):
        """Fetch the original metadata for the given index before normalization."""
        return self.metadata.iloc[idx].to_dict()
