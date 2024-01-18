from tqdm.contrib import tzip
from sklearn.ensemble import IsolationForest
import pandas as pd


def train_iforest(train_df, test_df, event_title, test_dates):
    anomalies_list = []
    for idx, train, test in tzip(
        train_df.index,
        train_df.values,
        test_df.values,
        desc=f"Fitting Isolation Forest for {event_title}",
    ):
        train, test = train.reshape(-1, 1), test.reshape(-1, 1)
        iforest = IsolationForest(n_jobs=-1)
        iforest.fit(train)
        y_pred = iforest.predict(test)
        anomaly_idx = y_pred == -1

        anomalies = pd.DataFrame(
            test_dates[anomaly_idx], columns=["target_dates"]
        ).assign(target_indices=idx)
        anomalies_list.append(anomalies)
    return pd.concat(anomalies_list)
