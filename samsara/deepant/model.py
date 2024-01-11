import torch
import torch.nn as nn
import lightning as L


class DeepAnt(nn.Module):
    def __init__(self, p_w):
        super().__init__()

        self.convblock1 = nn.Sequential(
            nn.Conv1d(in_channels=1, out_channels=32, kernel_size=3, padding="valid"),
            nn.ReLU(inplace=True),
            nn.MaxPool1d(kernel_size=2),
        )

        self.convblock2 = nn.Sequential(
            nn.Conv1d(in_channels=32, out_channels=32, kernel_size=3, padding="valid"),
            nn.ReLU(inplace=True),
            nn.MaxPool1d(kernel_size=2),
        )

        self.flatten = nn.Flatten()

        self.denseblock = nn.Sequential(
            nn.Linear(32, 40),
            # nn.Linear(96, 40), # for SEQL_LEN = 20
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.25),
        )
        self.out = nn.Linear(40, p_w)

    def forward(self, x):
        x = self.convblock1(x)
        x = self.convblock2(x)
        x = self.flatten(x)
        x = self.denseblock(x)
        x = self.out(x)
        return x


class ForecastBasedAD(L.LightningModule):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.criterion = nn.MSELoss()  # Debería ser MAE

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        X, y = batch
        y_pred = self(X).squeeze()
        loss = self.criterion(y_pred, y)
        self.log("train_loss", loss, prog_bar=True, logger=True)
        return loss

    def predict_step(self, batch, batch_idx):
        X, y = batch
        y_pred = self(X)
        pred_loss = torch.sqrt((y - y_pred.squeeze()) ** 2)
        return y_pred, pred_loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=3e-4)
