import torch
import lightning.pytorch as pl

from torch import nn
from torch.nn import functional as F
from torch import optim
from icecream import ic


class ResidualUnit(nn.Module):
    def __init__(self, in_features, out_features):
        super(ResidualUnit, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, out_features),
            nn.BatchNorm1d(out_features),
            nn.ReLU(),
            nn.Linear(out_features, out_features),
            nn.BatchNorm1d(out_features),
        )

    def forward(self, x):
        return F.leaky_relu(self.net(x))


class ResidualNetwork(nn.Module):
    def __init__(self, in_features, hidden_size, out_features, num_layers=4):
        super(ResidualNetwork, self).__init__()
        self.net = nn.Sequential(
            nn.Sequential(
                nn.Linear(in_features, hidden_size),
                nn.ReLU(),
            ),
            nn.Sequential(
                *[ResidualUnit(hidden_size, hidden_size) for _ in range(num_layers)]
            ),
            nn.Linear(hidden_size, out_features),
        )

    def forward(self, x):
        return self.net(x)


class MLP(nn.Module):
    def __init__(self, input_size, hidden_size, out_fatures, dropout_prob=0.5):
        super(MLP, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.SELU(),
            nn.Linear(hidden_size, hidden_size),
            nn.SELU(),
            nn.Dropout(dropout_prob),
            nn.Linear(hidden_size, hidden_size),
            nn.SELU(),
            nn.Dropout(dropout_prob),
            nn.Linear(hidden_size, out_fatures),
        )
    
    def forward(self, x):
        return self.net(x)

class BasicModule(pl.LightningModule):
    def __init__(
        self,
        model_constructor,
        in_features,
        hidden_size,
        out_features,
        lr=0.001,
        class_weights: torch.Tensor = None,
        criterion: nn.CrossEntropyLoss = nn.CrossEntropyLoss,
        model_constructor_kwargs={},
    ):
        super(BasicModule, self).__init__()
        self.save_hyperparameters(ignore=["class_weights"])
        self.constructor_kwargs = model_constructor_kwargs
        self.constructor = model_constructor(
            in_features, hidden_size, out_features, **self.constructor_kwargs
        )
        self.criterion_type = criterion
        self.criterion = (
            criterion(weight=class_weights)
            if class_weights is not None
            else criterion()
        )
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
        self.log("val_loss", loss, prog_bar=True, sync_dist=True)
        self.log("val_acc", acc, prog_bar=True, sync_dist=True)
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
        # import wandb
        from matplotlib import pyplot as plt
        from dvclive import Live
        from torchmetrics import ConfusionMatrix
        from sklearn.metrics import ConfusionMatrixDisplay

        cm_metric = ConfusionMatrix(num_classes=self.num_classes, task="multiclass").to(
            preds.device
        )
        cm = cm_metric(preds, labels).cpu().numpy()

        disp = ConfusionMatrixDisplay(
            confusion_matrix=cm, display_labels=range(self.num_classes)
        )
        fig, ax = plt.subplots(figsize=(8, 8))
        disp.plot(ax=ax, cmap="Blues")
        plt.title(f"{stage.capitalize()} Confusion Matrix")

        Live().log_image(f"{stage}_confusion_matrix.png", fig)
        # wandb.log({f"{stage}_confusion_matrix": wandb.Image(f"dvclive/plots/images/{stage}_confusion_matrix.png")})  # noqa: E501
        plt.close(fig)

    def configure_optimizers(self):
        return optim.Adam(self.parameters(), lr=self.lr)
