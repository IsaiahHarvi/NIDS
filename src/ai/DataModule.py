import os
import torch
import numpy as np
import lightning.pytorch as pl
import pandas as pd
from torch.utils.data import DataLoader, Dataset, Subset
from sklearn.utils.class_weight import compute_class_weight
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import StandardScaler, LabelEncoder
from icecream import ic
from collections import Counter


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
        num_workers: int = (os.cpu_count() // 2),
    ):
        super().__init__()
        self.paths = paths
        self.batch_size = batch_size
        self.val_split = val_split
        self.num_workers = num_workers
        self.scaler = StandardScaler()  # TODO: Parameterize this

    def setup(self):
        dfs: list[pd.DataFrame] = []
        for path in self.paths:
            df: pd.DataFrame = pd.read_csv(path)
            df.columns = df.columns.str.strip().str.replace(" ", "_")
            dfs.append(df)

        df = pd.concat(dfs, ignore_index=True)

        drop_columns = [
            'Flow_ID', 'Timestamp', 'Bwd_Avg_Packets/Bulk', 'Bwd_Avg_Bulk_Rate',
            'Bwd_PSH_Flags', 'Bwd_URG_Flags', 'Fwd_Avg_Bytes/Bulk', 'Fwd_Avg_Packets/Bulk',
            'Fwd_Avg_Bulk_Rate', 'Bwd_Avg_Bytes/Bulk', 'Fwd_Header_Length.1'
        ]
        change_ip = lambda x: sum([256**j*int(i) for j, i in enumerate(x.split('.')[::-1])])
        df["Source_IP"] = df["Source_IP"].apply(change_ip)
        df["Destination_IP"] = df["Destination_IP"].apply(change_ip)

        df = df.drop(drop_columns, axis=1, errors="ignore")
        df = df.replace([np.inf, -np.inf], np.nan).dropna()

        x = df.select_dtypes(include=[float, int])
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(df["Label"])
        ic(f"Label mapping: {dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))}")

        class_weights = compute_class_weight(
            "balanced", classes=np.unique(y), y=y
        )
        self.class_weights = torch.tensor(class_weights, dtype=torch.float32)

        self.n_classes = len(np.unique(y))
        self.example_shape = x.shape[1]

        x = self.scaler.fit_transform(x)

        dataset = CIC_IDS(x, y)
        shuffle_split = StratifiedShuffleSplit(n_splits=1, test_size=self.val_split)
        train_idx, val_idx = next(shuffle_split.split(x, y))

        train_distribution = Counter(y[train_idx])
        val_distribution = Counter(y[val_idx])

        ic(f"{train_distribution=}")
        ic(f"{val_distribution=}")

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
