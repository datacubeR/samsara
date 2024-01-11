import matplotlib.pyplot as plt


def show_pred_info(ts, preds, target_indices, is_right=True):
    name = target_indices.split("-")[0]
    if is_right:
        output = preds.query("target_indices == @target_indices and is_right")
    else:
        output = preds.query("target_indices == @target_indices")
    dates = output.target_dates.tolist()
    ts[name].loc[target_indices].plot(figsize=(20, 6))
    plt.vlines(x=dates, ymin=-1, ymax=1, color="red", alpha=0.2)
    plt.title(target_indices)
    plt.show()
    return output
