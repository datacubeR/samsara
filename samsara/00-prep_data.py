import pandas as pd
from loguru import logger

PATHS = [
    "ESTABLE_Arboreo_timeSeries/ESTABLE_TimeSerie_ndvi.csv",
    "INCENDIO_Arboreo_timeSeries/INCENDIO_TimeSerie_ndvi.csv",
    "SEQUIA_Arboreo_timeSeries/SEQUIA_TimeSerie_ndvi.csv",
    "TALA_Arboreo_timeSeries/TALA_TimeSerie_ndvi.csv",
    "VARIOS_Arboreo_timeSeries/VARIOS_TimeSerie_ndvi.csv",
]
OUTPUT_PATH = "data/ts_bosques.parquet"


def import_data(file_path):
    event = file_path.split("_")[0]
    logger.info(f"Importando datos de {event}...")
    df = pd.read_csv(file_path, index_col=0)
    df["event"] = event
    logger.info(f"{event}: {df.shape}")
    return df


if __name__ == "__main__":
    df_list = []
    for path in PATHS:
        df_list.append(import_data(path))

    ## Concatena y ordena las columnas por fecha.
    logger.info("Concatenando datos...")
    df = pd.concat(df_list)
    columns = df.columns.sort_values()
    df = df[columns]

    logger.info("Exportando Datos finales a Parquet...")
    df.to_parquet(OUTPUT_PATH, index=False)

    logger.info(f"Datos Correctamente exportados a Parquet a {OUTPUT_PATH}: {df.shape}")
