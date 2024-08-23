import torch
import torch.nn as nn
import torch.optim as optim
import lightning.pytorch as pl


def RNN(in_features, hidden_size, batch_first=True):
    return nn.RNN(in_features, hidden_size, batch_first=batch_first)


class BasicModule(pl.LightningModule):
    def __init__(self, model_constructor, in_features, hidden_size, out_features, lr=0.001):
        super(BasicModule, self).__init__()
        self.save_hyperparameters()
        self.constructor = model_constructor(in_features, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, out_features)
        self.criterion = nn.CrossEntropyLoss()
        self.lr = lr

    def forward(self, x):
        h0 = torch.zeros(1, x.size(0), self.hparams.hidden_size).to(x.device)
        out, _ = self.constructor(x, h0)
        out = self.fc(out[:, -1, :])
        return out

    def training_step(self, batch, batch_idx):
        x, y = batch
        outputs = self(x)
        loss = self.criterion(outputs, y)
        self.log('train_loss', loss)
        return loss

    def test_step(self, batch, batch_idx):
        pass

    def validation_step(self, batch, batch_idx):
        x, y = batch
        outputs = self(x)
        loss = self.criterion(outputs, y)
        acc = (outputs.argmax(dim=1) == y).float().mean()
        self.log('val_loss', loss, prog_bar=True)
        self.log('val_acc', acc, prog_bar=True)

    def configure_optimizers(self):
        return optim.Adam(self.parameters(), lr=self.lr)

