import numpy as np
import pandas as pd
from loguru import logger

from .sliding import create_sequences


def train_test_sequences(event, resample, interpolation, seq_len):
    logger.info(f"Cargando Datos: {resample}/{interpolation} para {event}...")
    df = pd.read_parquet(
        f"data/resample/resample_{event}_{resample}_{interpolation}.parquet"
    )

    logger.info(f"Definiendo Series de Train y Test para {event}...")
    train_columns = np.load(
        f"data/train/{event}_train_{resample}_{interpolation}.npy", allow_pickle=True
    )
    test_columns = np.load(
        f"data/test/{event}_test_{resample}_{interpolation}.npy", allow_pickle=True
    )
    df_train = df[train_columns]
    df_test = df[test_columns]

    logger.info(f"Creando Secuencias para {event}...")
    train_data = {}
    (
        train_data["sequences"],
        train_data["slide_dates"],
        train_data["ts_indices"],
        train_data["forecast_values"],
    ) = create_sequences(df_train, seq_len=seq_len)

    test_data = {}
    (
        test_data["sequences"],
        test_data["slide_dates"],
        test_data["ts_indices"],
        test_data["forecast_values"],
    ) = create_sequences(df_test, seq_len=seq_len)

    logger.success(
        f"Train {event} creado Exitosamente: {train_data['sequences'].shape}"
    )
    logger.success(f"Test {event} creado Exitosamente: {test_data['sequences'].shape}")

    return train_data, test_data
