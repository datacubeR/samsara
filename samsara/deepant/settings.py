from .data import DataModule
from .model import ForecastBasedAD
import lightning as L
from lightning.pytorch.callbacks import ModelCheckpoint


def deepant_settings(model, train_set, test_set, settings, train=False):
    anomaly_detector = ForecastBasedAD(model)
    dm = DataModule(
        train_sequences=train_set["sequences"],
        train_targets=train_set["targets"],
        val_sequences=test_set["sequences"],
        val_targets=test_set["targets"],
        batch_size=settings["batch_size"],
        nw=settings["nw"],
    )

    mc = ModelCheckpoint(
        dirpath="checkpoints",
        save_last=True,
        save_top_k=1,
        verbose=True,
        monitor="train_loss",
        mode="min",
    )

    mc.CHECKPOINT_NAME_LAST = f"{settings['name']}-best-checkpoint"

    trainer = L.Trainer(
        max_epochs=settings["batch_size"],
        accelerator="gpu",
        devices=1,
        callbacks=[mc],
        # progress_bar_refresh_rate=30,
        fast_dev_run=settings["fast_dev_run"],
        overfit_batches=settings["overfit_batches"],
    )

    if train:
        trainer.fit(anomaly_detector, dm)

    return trainer, anomaly_detector, dm
