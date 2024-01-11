import torch
from torch.utils.data import Dataset, DataLoader
import lightning as L


class ForecastBasedDataset(Dataset):
    def __init__(self, sequences, targets):
        self.sequences = sequences
        self.targets = targets

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        # Sequences (B, seq_len, 1)
        return (
            torch.tensor(self.sequences[idx], dtype=torch.float).reshape(1, -1),
            torch.tensor(self.targets[idx], dtype=torch.float),
        )


class DataModule(L.LightningDataModule):
    def __init__(
        self,
        train_sequences,
        train_targets,
        val_sequences,
        val_targets,
        batch_size=32,
        nw=8,
    ):
        super().__init__()
        self.train_sequences = train_sequences
        self.train_targets = train_targets
        self.val_sequences = val_sequences
        self.val_targets = val_targets
        self.batch_size = batch_size
        self.nw = nw

    def setup(self, stage=None):
        self.train_dataset = ForecastBasedDataset(
            self.train_sequences, self.train_targets
        )
        self.val_dataset = ForecastBasedDataset(self.val_sequences, self.val_targets)

    def train_dataloader(self):
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            num_workers=self.nw,
            pin_memory=True,
            shuffle=False,
        )

    def test_dataloader(self):
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            num_workers=self.nw,
            pin_memory=True,
            shuffle=False,
        )

    def predict_dataloader(self):
        return DataLoader(
            self.val_dataset,
            batch_size=self.batch_size,
            num_workers=self.nw,
            pin_memory=True,
            shuffle=False,
        )
