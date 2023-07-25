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


def create_heatmap_df(dict, ex_col, resample=None):
    output_dict = {}

    for name, data in dict.items():
        if resample is not None:
            data = data.drop(columns=ex_col).T
            data.index = pd.to_datetime(data.index)
            data = data.resample(resample).mean()
        else:
            data = data.drop(columns=ex_col).T
        output_dict[name] = data.T.notnull().sum().astype(bool)
        output_dict[name].name = name

    output = pd.concat(output_dict.values(), axis=1).fillna(False).sort_index()
    # output.index = pd.to_datetime(output.index)
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


if __name__ == "__main__":
    df_dict = import_data()
    ex_col = ["not_null", "not_null_perc"]
    output_dict = {}
    for name, data in df_dict.items():
        data = data.drop(columns=ex_col).T
        print(data.index)
        data.index = pd.to_datetime(data.index)
        data = data.resample("W").mean()
        print("Muestra de Datos:", data)
        output_dict[name] = data.T.notnull().sum().astype(bool)
        output_dict[name].name = name

    output_dict
