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
from torch.utils.data import DataLoader, Dataset, WeightedRandomSampler
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler


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
        dfs = []
        for path in self.paths:
            df = pd.read_csv(path, delimiter="\t", low_memory=False)
            df.columns = df.columns.str.strip().str.replace(" ", "_")
            dfs.append(df)

        df = pd.concat(dfs, ignore_index=True)
        df["label"] = df["label"].str.lower().str.replace(r"[\s-]+", "_", regex=True)
        df["label"] = df["label"].replace({"portscan": "port_scan"})
        y = df["label"].to_numpy()

        self.metadata = df.copy()
        df.drop(
            [col for col in df.columns if "piat" not in col.lower()],
            axis=1,
            errors="ignore",
            inplace=True,
        )

        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y)
        ic(
            f"Label to index mapping: {dict(zip(label_encoder.classes_, range(len(label_encoder.classes_))))}"
        )

        df = df.replace([np.inf, -np.inf], np.nan).dropna()
        x = df.select_dtypes(include=[float, int]).to_numpy()
        self.example_shape = x.shape[1]

        x = self.scaler.fit_transform(x)

        shuffle_split = StratifiedShuffleSplit(
            n_splits=1, test_size=self.val_split, random_state=42
        )
        train_idx, val_idx = next(shuffle_split.split(x, y))

        x_train, y_train = x[train_idx], y[train_idx]
        x_val, y_val = x[val_idx], y[val_idx]
        assert (
            len(set(list(Counter(y_train).keys())) - set(list(Counter(y_val).keys())))
            == 0
        )

        ic(f"Original class distribution: {Counter(y_train)}")
        undersample_strategy = {0: 750_000}
        oversample_strategy = {
            1: 5000,
            2: 112_833,
            3: 8326,
            4: 150_000,
            5: 5000,
            6: 10188,
            7: 5000,
            8: 5000,
            9: 5000,
            10: 178869,
            11: 5000,
            12: 5000,
            13: 5000,
            14: 5000,
        }
        pipeline = Pipeline([
            ("under", RandomUnderSampler(sampling_strategy=undersample_strategy, random_state=42)),
            ("smote", SMOTE(sampling_strategy=oversample_strategy, random_state=42))
        ])
        x_train, y_train = pipeline.fit_resample(x_train, y_train)

        ic(f"Resampled class distribution: {Counter(y_train)}")

        class_weights = compute_class_weight(
            "balanced", classes=np.unique(y_train), y=y_train
        )
        self.class_weights = torch.tensor(class_weights, dtype=torch.float32)
        self.n_classes = len(np.unique(y_train))

        self.train_dataset = CIC_IDS(x_train, y_train)
        self.val_dataset = CIC_IDS(x_val, y_val)

        self.val_idx = val_idx

    def train_dataloader(self) -> DataLoader:
        train_weights = [
            self.class_weights[label.item()] for label in self.train_dataset.labels
        ]
        train_sampler = WeightedRandomSampler(
            train_weights, num_samples=len(self.train_dataset), replacement=True
        )

        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            sampler=train_sampler,
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
        return self.metadata.iloc[idx].to_dict()
