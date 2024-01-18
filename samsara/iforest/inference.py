from .model import train_iforest
import pandas as pd


def detect_anomalies(train_df_dict, test_df_dict, paths, test_dates):
    anomalies = []

    for event in paths:
        train_df = train_df_dict[event]
        test_df = test_df_dict[event]
        output = train_iforest(train_df, test_df, event, test_dates=test_dates)
        anomalies.append(output)

    anomalies_df = pd.concat(anomalies)
    anomalies_df[["NAME", "IDpix", "ID"]] = anomalies_df.target_indices.str.split(
        "-", expand=True
    )
    anomalies_df[["IDpix", "ID"]] = anomalies_df[["IDpix", "ID"]].astype("int64")
    anomalies_df = anomalies_df[
        ["target_indices", "target_dates", "NAME", "IDpix", "ID"]
    ]
    return anomalies_df
