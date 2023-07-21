import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from loguru import logger

logger.info("Importando Datos desde Parquet...")
df = pd.read_parquet("data/ts_bosques.parquet")
logger.info(f"Datos importados correctamente {df.shape}")

print(df.groupby("event").size().sort_values(ascending=False))

print("Fechas Mínima y Máxima")
print(f"Minimo {np.min(df.columns[:-2])}")
print(f"Máximo {np.max(df.columns[:-2])}")
df.columns[:-2].astype("datetime64[ns]")

## Calcular Semanas
semanas = pd.Series(df.columns[:-2].astype("datetime64[ns]")).dt.isocalendar()
print("Mediciones por Semana")
semanas[["year", "week"]].value_counts()

df.notnull().sum().iloc[:-2].plot(title="Valores No Nulos")
plt.show()

notnull_df = df.drop(columns=["event", "IDpix"]).notnull().sum(axis=1).to_frame()
notnull_df["event"] = df["event"]

print(notnull_df.groupby("event").agg(["mean", "min", "max"]))
