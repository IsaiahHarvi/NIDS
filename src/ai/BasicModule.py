import torch
import torch.nn as nn
import torch.optim as optim
import lightning.pytorch as pl

import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt

import numpy as np
from torchmetrics import ConfusionMatrix
from sklearn.metrics import ConfusionMatrixDisplay
from dvclive import Live


class RNN(nn.Module):
    def __init__(self, in_features, hidden_size, batch_size, batch_first=True):
        super(RNN, self).__init__()
        self.rnn = nn.RNN(in_features, hidden_size, batch_first=batch_first)
        self.hidden_size = hidden_size
        self.batch_size = batch_size

    def forward(self, x):
        h0 = torch.zeros(1, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.rnn(x, h0)
        return out[:, -1, :]
    

class BasicModule(pl.LightningModule):
    def __init__(self, model_constructor, in_features, hidden_size, out_features, batch_size, lr=0.001):
        super(BasicModule, self).__init__()
        self.save_hyperparameters()
        self.constructor = model_constructor(in_features, hidden_size, batch_size)
        self.linear = nn.Linear(hidden_size, out_features)
        self.criterion = nn.CrossEntropyLoss()
        self.lr = lr
        self.validation_outputs = []
        self.test_outputs = []
        self.num_classes = out_features

    def forward(self, x):
        return self.linear(
            self.constructor(x)
        )

    def training_step(self, batch, batch_idx):
        x, y = batch
        outputs = self(x)
        loss = self.criterion(outputs, y)
        acc = (outputs.argmax(dim=1) == y).float().mean()
        self.log("train_loss", loss, prog_bar=True)
        self.log("train_acc", acc, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        outputs = self(x)
        loss = self.criterion(outputs, y)
        preds = outputs.argmax(dim=1)
        acc = (preds == y).float().mean()
        self.log("val_loss", loss, prog_bar=True)
        self.log("val_acc", acc, prog_bar=True)
        self.validation_outputs.append((preds, y))
        return loss

    def on_validation_epoch_end(self):
        preds = torch.cat([x[0] for x in self.validation_outputs])
        targets = torch.cat([x[1] for x in self.validation_outputs])
        self.log_confusion_matrix(preds, targets, "val")
        self.validation_outputs.clear()

    def test_step(self, batch, batch_idx):
        x, y = batch
        outputs = self(x)
        loss = self.criterion(outputs, y)
        preds = outputs.argmax(dim=1)
        acc = (preds == y).float().mean()
        self.log("test_loss", loss, prog_bar=True)
        self.log("test_acc", acc, prog_bar=True)
        self.test_outputs.append((preds, y))
        return loss

    def on_test_epoch_end(self):
        preds = torch.cat([x[0] for x in self.test_outputs])
        targets = torch.cat([x[1] for x in self.test_outputs])
        self.log_confusion_matrix(preds, targets, "test")
        self.test_outputs.clear()

    def on_fit_end(self):
        self.on_validation_epoch_end()
        self.on_test_epoch_end()

    def log_confusion_matrix(self, preds, labels, stage):
        cm = ConfusionMatrix(num_classes=self.num_classes, task="multiclass")(preds, labels).cpu().numpy()

        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=range(self.num_classes))
        fig, ax = plt.subplots(figsize=(8, 8))
        disp.plot(ax=ax, cmap="Blues")
        plt.title(f"{stage.capitalize()} Confusion Matrix")

        live = Live()
        live.log_image(f"{stage}_confusion_matrix.png", fig)
        plt.close(fig)

    def configure_optimizers(self):
        return optim.Adam(self.parameters(), lr=self.lr)
