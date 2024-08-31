import torch
import lightning.pytorch as pl

from torch import nn
from torch import optim
from icecream import ic


class ResidualBlock(nn.Module):
    def __init__(self, in_features, hidden_size):
        super(ResidualBlock, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, hidden_size),
            nn.BatchNorm1d(hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, in_features),
            nn.BatchNorm1d(in_features),
        )

    def forward(self, x):
        out = self.net(x)
        return nn.LeakyReLU()(out + x)


class ResidualNetwork(pl.LightningModule):
    def __init__(self, in_channels, hidden_size, out_features, num_blocks=3):
        super(ResidualNetwork, self).__init__()
        self.save_hyperparameters()

        self.conv_layer = nn.Conv1d(1, in_channels, kernel_size=3, padding=1)
        self.flatten_size = in_channels * 80
        self.linear_layer = nn.Linear(self.flatten_size, hidden_size)
        self.residual_blocks = nn.Sequential(
            *[ResidualBlock(hidden_size, hidden_size) for _ in range(num_blocks)]
        )
        self.output_layer = nn.Linear(hidden_size, out_features)

    def forward(self, x):
        x = self.conv_layer(x)
        x = x.view(x.size(0), -1)
        x = self.linear_layer(x) 
        x = self.residual_blocks(x)
        x = self.output_layer(x)
        return x

class BasicModule(pl.LightningModule):
    def __init__(
        self,
        model_constructor,
        in_features,
        hidden_size,
        out_features,
        lr=0.001,
        model_constructor_kwargs={},
    ):
        super(BasicModule, self).__init__()
        self.save_hyperparameters()
        self.constructor = model_constructor(
            in_features, hidden_size, out_features, **model_constructor_kwargs
        )
        self.criterion = nn.CrossEntropyLoss()
        self.lr = lr
        self.validation_outputs = []
        self.test_outputs = []
        self.num_classes = out_features

    def forward(self, x):
        return self.constructor(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        if y.ndim > 1 and y.size(1) == self.num_classes:
            y = torch.argmax(y, dim=1)

        outputs = self(x)
        loss = self.criterion(outputs, y)
        acc = (outputs.argmax(dim=1) == y).float().mean()
        self.log("train_loss", loss, prog_bar=True)
        self.log("train_acc", acc, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        if y.ndim > 1 and y.size(1) == self.num_classes:
            y = torch.argmax(y, dim=1)

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
        if y.ndim > 1 and y.size(1) == self.num_classes:
            y = torch.argmax(y, dim=1)

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

    def log_confusion_matrix(self, preds, labels, stage):
        # we import here to minimize the deps in the model service
        import matplotlib
        matplotlib.use("Agg")
        from matplotlib import pyplot as plt
        from dvclive import Live
        from torchmetrics import ConfusionMatrix
        from sklearn.metrics import ConfusionMatrixDisplay

        cm_metric = ConfusionMatrix(num_classes=self.num_classes, task="multiclass").to(preds.device)
        cm = cm_metric(preds, labels).cpu().numpy()

        disp = ConfusionMatrixDisplay(
            confusion_matrix=cm, display_labels=range(self.num_classes)
        )
        fig, ax = plt.subplots(figsize=(8, 8))
        disp.plot(ax=ax, cmap="Blues")
        plt.title(f"{stage.capitalize()} Confusion Matrix")

        live = Live()
        live.log_image(f"{stage}_confusion_matrix.png", fig)
        plt.close(fig)

    def configure_optimizers(self):
        return optim.Adam(self.parameters(), lr=self.lr)
