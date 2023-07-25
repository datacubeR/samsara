from pathlib import Path

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


def import_to_parquet(file_path):
    # Extracción del nombre del Evento
    event = file_path.split("_")[0]
    # Extraigo información del Path para exportar los datos.
    stem = Path(file_path).stem
    logger.info(f"Importando datos de {event}...")
    df = pd.read_csv(file_path, index_col=0)
    logger.info(f"{event}: {df.shape}, Exportando datos a Parquet...")
    df.to_parquet(f"data/{stem}.parquet", index=False)


if __name__ == "__main__":
    df_list = []
    for path in PATHS:
        import_to_parquet(path)

    logger.info("Proceso Terminado con Éxito.")
