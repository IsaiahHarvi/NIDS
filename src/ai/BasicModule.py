import torch
import torch.nn as nn
import torch.optim as optim
import lightning.pytorch as pl


def RNN(x, in_features, hidden_size, batch_size, batch_first=True):
    rnn = nn.RNN(in_features, hidden_size, batch_first=batch_first)
    h0 = torch.zeros(1, batch_size, hidden_size).to(x.device)
    out, _ = rnn(x, h0)
    return out[:, -1, :]


class BasicModule(pl.LightningModule):
    def __init__(self, model_constructor, in_features, hidden_size, out_features, lr=0.001, batch_size=64):
        super(BasicModule, self).__init__()
        self.save_hyperparameters()
        self.constructor = model_constructor
        self.batch_size = batch_size # needefd for h0
        self.fc = nn.Linear(hidden_size, out_features)
        self.criterion = nn.CrossEntropyLoss()
        self.lr = lr

    def forward(self, x):
        return self.fc(
            self.constructor(x, self.hparams.in_features, self.hparams.hidden_size, self.batch_size)
        )

    def training_step(self, batch, batch_idx):
        x, y = batch
        outputs = self(x)
        loss = self.criterion(outputs, y)
        acc = (outputs.argmax(dim=1) == y).float().mean()
        self.log('train_loss', loss, prog_bar=True)
        self.log('train_acc', acc, prog_bar=True)

    def test_step(self, batch, batch_idx):
        x, y = batch
        outputs = self(x)
        loss = self.criterion(outputs, y)
        acc = (outputs.argmax(dim=1) == y).float().mean()
        self.log('test_loss', loss, prog_bar=True)
        self.log('test_acc', acc, prog_bar=True)

    def validation_step(self, batch, batch_idx):
        x, y = batch
        outputs = self(x)
        loss = self.criterion(outputs, y)
        acc = (outputs.argmax(dim=1) == y).float().mean()
        self.log('val_loss', loss, prog_bar=True)
        self.log('val_acc', acc, prog_bar=True)

    def configure_optimizers(self):
        return optim.Adam(self.parameters(), lr=self.lr)

