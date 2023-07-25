import pandas as pd
import streamlit as st


@st.cache_data
def import_data():
    """
    Returns
    -------

        Retorna un Diccionario con los Datasets de cada Evento.
    """
    output = dict(
        ESTABLE=pd.read_parquet("data/ESTABLE_TimeSerie_ndvi.parquet").set_index(
            "IDpix"
        ),
        INCENDIO=pd.read_parquet("data/INCENDIO_TimeSerie_ndvi.parquet").set_index(
            "IDpix"
        ),
        SEQUIA=pd.read_parquet("data/SEQUIA_TimeSerie_ndvi.parquet").set_index("IDpix"),
        TALA=pd.read_parquet("data/TALA_TimeSerie_ndvi.parquet").set_index("IDpix"),
        VARIOS=pd.read_parquet("data/VARIOS_TimeSerie_ndvi.parquet").set_index("IDpix"),
    )

    for name, data in output.items():
        output[name]["not_null"] = data.notnull().sum(axis=1)
        output[name]["not_null_perc"] = data.notnull().sum(axis=1) / data.shape[1] * 100
    return output


def index_to_week(df):
    """
    Parameters
    ----------
    df : DataFrame al que se le quiere transformar los Índices de Fecha a Semana. Debe tener un índice con Fechas.


    Returns
    -------

       Devuelve una Serie de Índices de Strings con formato "YYYY-WW" donde YYYY es el año y WW es la semana del año.
    """
    calendar = pd.Series(df.index).astype("datetime64[ns]").dt.isocalendar()
    new_index = calendar.year.astype(str) + "-" + calendar.week.astype(str)
    return new_index
