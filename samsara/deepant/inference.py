import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def run_inference(trainer, model, dm):
    output_val = trainer.predict(model=model, datamodule=dm)
    val_losses = []
    preds = []
    for pred, loss in output_val:
        val_losses.extend(loss.numpy())
        preds.extend(pred.numpy())
    val_losses = np.array(val_losses)
    preds = np.array(preds)
    return preds, val_losses


def plot_losses(losses):
    threshold = losses.mean() + 3 * losses.std()
    plt.figure(figsize=(20, 6))
    plt.hist(losses, bins=50)

    return threshold


def detect_anomalies(test_set, losses, threshold):
    idx = losses >= threshold
    predictions = pd.DataFrame(
        dict(
            target_indices=test_set["target_indices"][idx],
            target_dates=test_set["target_dates"][idx],
        )
    )
    predictions[["NAME", "IDpix", "ID"]] = predictions.target_indices.str.split(
        "-", expand=True
    )
    predictions[["IDpix", "ID"]] = predictions[["IDpix", "ID"]].astype("int64")
    return predictions
