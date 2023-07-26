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
        ESTABLE=pd.read_parquet("data/raw/ESTABLE_TimeSerie_ndvi.parquet").set_index(
            "IDpix"
        ),
        INCENDIO=pd.read_parquet("data/raw/INCENDIO_TimeSerie_ndvi.parquet").set_index(
            "IDpix"
        ),
        SEQUIA=pd.read_parquet("data/raw/SEQUIA_TimeSerie_ndvi.parquet").set_index(
            "IDpix"
        ),
        TALA=pd.read_parquet("data/raw/TALA_TimeSerie_ndvi.parquet").set_index("IDpix"),
        VARIOS=pd.read_parquet("data/raw/VARIOS_TimeSerie_ndvi.parquet").set_index(
            "IDpix"
        ),
    )

    for name, data in output.items():
        output[name]["not_null"] = data.notnull().sum(axis=1)
        output[name]["not_null_perc"] = data.notnull().sum(axis=1) / data.shape[1] * 100
    return output


def create_heatmap_df(dict, ex_col, resample=None):
    """

    Parameters
    ----------
    dict : Diccionario de DataFrames con los Datos de Series de Tiempo de cada Evento.

    ex_col : Lista de Columnas que no son Fechas en la Serie de Tiempo.

    resample : str, optional representa el resample a aplicar.


    Returns
    -------
    output: Corresponde a la concatención de todos los eventos.
    Está indexado por fecha (original o resampleada) y cada columna representa un evento.

    """
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


def create_histogram(event, color):
    plot = (
        st.session_state.df_dict[event]["not_null_perc"]
        .plot(
            kind="hist",
            title="Histograma de % de Valores No Nulos",
            color=color,
            edgecolor="black",
            bins=100,
        )
        .figure
    )
    return st.pyplot(plot, clear_figure=True)


def summary_data(evento):
    container = st.container()
    container.header(evento)
    container.metric(
        label="Dimensiones", value=f"{st.session_state.df_dict[evento].shape}"
    )
    container.metric(
        label="Mediciones Promedio",
        value=f"{st.session_state.df_dict[evento]['not_null'].mean():.0f}/{st.session_state.df_dict[evento]['not_null_perc'].mean():.0f}%",
    )
    container.metric(
        label="Mínimo de Mediciones",
        value=f"{st.session_state.df_dict[evento]['not_null'].min():.0f}/{st.session_state.df_dict[evento]['not_null_perc'].min():.0f}%",
    )
    container.metric(
        label="Máximo de Mediciones",
        value=f"{st.session_state.df_dict[evento]['not_null'].max():.0f}/{st.session_state.df_dict[evento]['not_null_perc'].max():.0f}%",
    )
    return container


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
