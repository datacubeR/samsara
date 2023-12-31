import pandas as pd


def import_raw_data():
    """
    Returns
    -------

        Retorna un Diccionario con los Datasets de cada Evento.
        Transforma las columnas al formato "EVENTO-IDPix" y los
        index a Datetime para poder generar el resample apropiado.
    """
    output = dict(
        ESTABLE=pd.read_parquet("data/raw/ESTABLE_TimeSerie_ndvi.parquet")
        .set_index("IDpix")
        .T,
        INCENDIO=pd.read_parquet("data/raw/INCENDIO_TimeSerie_ndvi.parquet")
        .set_index("IDpix")
        .T,
        SEQUIA=pd.read_parquet("data/raw/SEQUIA_TimeSerie_ndvi.parquet")
        .set_index("IDpix")
        .T,
        TALA=pd.read_parquet("data/raw/TALA_TimeSerie_ndvi.parquet")
        .set_index("IDpix")
        .T,
        VARIOS=pd.read_parquet("data/raw/VARIOS_TimeSerie_ndvi.parquet")
        .set_index("IDpix")
        .T,
    )

    for event, _ in output.items():
        output[event].columns = [f"{event}-{col}" for col in output[event].columns]
        output[event].index = pd.to_datetime(output[event].index)
    return output
