import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42
TEST_SIZE = 0.2
EVENTOS = ["ESTABLE", "INCENDIO", "SEQUIA", "TALA", "VARIOS"]

TRAIN_PATH = Path("data/train")
TEST_PATH = Path("data/test")
TRAIN_PATH.mkdir(parents=True, exist_ok=True)
TEST_PATH.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--resample", "-r", choices=["W", "2W", "M"], required=True)
    parser.add_argument(
        "--interpolate", "-i", choices=["linear", "time", "ff", "bf"], required=True
    )
    args = parser.parse_args()

    logger.warning(
        f"Generando Split Train/Test: {100-TEST_SIZE*100:.0f}/{TEST_SIZE*100:.0f}"
    )
    for evento in EVENTOS:
        logger.info(f"Importando Datos de {evento}")
        df = pd.read_parquet(
            f"data/resample/resample_{evento}_{args.resample}_{args.interpolate}.parquet"
        )

        columns = df.columns.to_numpy()
        ts_train, ts_test = train_test_split(
            columns, test_size=TEST_SIZE, random_state=RANDOM_STATE
        )
        logger.success(f"Guardando Índices de Train para {evento}...")
        np.save(
            TRAIN_PATH / f"{evento}_train_{args.resample}_{args.interpolate}.npy",
            ts_train,
        )
        logger.success(f"Guardando Índices de Test para {evento}...")
        np.save(
            TEST_PATH / f"{evento}_test_{args.resample}_{args.interpolate}.npy", ts_test
        )

    logger.success(f"Proceso de Split finalizado con Éxito!")
