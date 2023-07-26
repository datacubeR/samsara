import numpy as np
import pandas as pd

from data import create_sequences, import_data

df_dict = import_data()

df_resample = df_dict["ESTABLE"].resample("M").mean()
df_interpolated = df_resample.interpolate(method="time")

print(f"Null Values: {df_interpolated.isnull().sum().sum()}")

SEQ_LEN = 5
# TODO: Este archivo tiene trabajo por delante aún.
# TODO: Faltan Opciones de Resampling e Interpolación.
dates = np.array(pd.date_range(start="2019-01-01", end="2020-01-01", freq="M"))
df = pd.DataFrame(
    np.random.randint(0, 10, size=(12, 2)),
    index=dates,
    columns=["ESTABLE-1", "ESTABLE-2"],
)
sequences, slide_dates, ts_indices = create_sequences(df, SEQ_LEN)
