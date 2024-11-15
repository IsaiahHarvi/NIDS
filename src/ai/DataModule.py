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
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline


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

        drop_columns = [
            "id",
            "expiration_id",
            "src_mac",
            "src_oui",
            "dst_mac",
            "dst_oui",
            "flow_id",
            "flow_start",
            "bidirectional_first_seen_ms",
            "bidirectional_last_seen_ms",
            "src2dst_first_seen_ms",
            "src2dst_last_seen_ms",
            "dst2src_first_seen_ms",
            "dst2src_last_seen_ms",
        ]
        df.drop(drop_columns, axis=1, errors="ignore", inplace=True)
        df = df[
            ~df["label"].isin(
                {"web_attack_brute_force", "web_attack_xss", "web_attack_sql_injection"}
            )
        ]  # remove webattack classes bc lazy

        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(df["label"])
        ic(
            f"Label to index mapping: {dict(zip(label_encoder.classes_, range(len(label_encoder.classes_))))}"
        )

        # Save pre-normalized metadata
        self.metadata = df.copy()
        df.drop(["src_ip", "dst_ip", "src_port", "dst_port"], axis=1, inplace=True)

        # dl = Counter(df["label"])
        df = df.replace([np.inf, -np.inf], np.nan).dropna()
        x = df.select_dtypes(include=[float, int]).to_numpy()
        self.example_shape = x.shape[1]

        # missing_classes = {key: value for key, value in dl.items() if key not in label_encoder.classes_}
        # ic("Missing Classes: ", missing_classes)
        df.drop("label", axis=1, inplace=True)

        x = self.scaler.fit_transform(x)

        shuffle_split = StratifiedShuffleSplit(
            n_splits=1, test_size=self.val_split, random_state=42
        )
        train_idx, val_idx = next(shuffle_split.split(x, y))

        x_train, y_train = x[train_idx], y[train_idx]
        x_val, y_val = x[val_idx], y[val_idx]

        label_to_index = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
        ss_over = {
            label_to_index[label]: count for label, count in {
                "dos_hulk": 200000,
                "ddos": 150000,
                "portscan": 130000,
                "dos_goldeneye": 10000,
                "ftp_patator": 10200,
                "dos_slowloris": 10200,
                "dos_slowhttptest": 10200,
                "ssh_patator": 5000,
                "bot": 3000,
                # "web_attack___brute_force": 2000,
                # "web_attack___xss": 1500,
                "infiltration": 1500,
                # "web_attack___sql_injection": 1500,
                "heartbleed": 1500,
            }.items() if label in label_to_index
        }
        ss_under = {
            label_to_index["benign"]: 50000
        }

        ic(f"Classes in y_train: {Counter(y_train)}")
        missing_classes = {
            cls for cls in ss_over if cls not in label_encoder.classes_
        }
        ic(f"Missing classes in y_train: {missing_classes}")

        over = SMOTE(sampling_strategy=ss_over, random_state=42)
        under = RandomUnderSampler(
            sampling_strategy=ss_under, random_state=42
        )
        pipeline = Pipeline(steps=[("oversample", over), ("undersample", under)])

        ic(f"Original class distribution: {Counter(y_train)}")
        x_train, y_train = pipeline.fit_resample(x_train, y_train)
        ic(f"Resampled class distribution: {Counter(y_train)}")

        self.train_dataset = CIC_IDS(x_train, y_train)
        self.val_dataset = CIC_IDS(x_val, y_val)

        class_weights = compute_class_weight(
            "balanced", classes=np.unique(y_train), y=y_train
        )
        self.class_weights = torch.tensor(class_weights, dtype=torch.float32)
        self.n_classes = len(np.unique(y_train))

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
