import pandas as pd
import streamlit as st
from pages.utils import import_data

st.set_page_config(layout="wide")
st.markdown("# EDA Samsara")

if "EXCLUDE_COLUMNS" not in st.session_state:
    st.session_state.EXCLUDE_COLUMNS = ["not_null", "not_null_perc"]

if "df_dict" not in st.session_state:
    st.session_state.df_dict = import_data()

col1, col2, col3, col4, col5 = st.columns(5)


def summary_data(evento):
    container = st.container()
    container.header(evento)
    container.metric(
        label="Dimensiones", value=f"{st.session_state.df_dict[evento].shape}"
    )
    container.metric(
        label="Porcentaje Medio de Mediciones",
        value=f"{st.session_state.df_dict[evento]['not_null_perc'].mean():.2f}%",
    )
    return container


with col1:
    summary_data("ESTABLE")
with col2:
    summary_data("INCENDIO")
with col3:
    summary_data("SEQUIA")
with col4:
    summary_data("TALA")
with col5:
    summary_data("VARIOS")


col1, col2 = st.columns(2)
df = pd.DataFrame(
    {name: data.shape for name, data in st.session_state.df_dict.items()},
    index=["Filas", "Columnas"],
)

with col1:
    plot0 = (
        df.loc["Filas"]
        .plot(kind="bar", title="Número de Filas", color="green", edgecolor="black")
        .figure
    )
    st.pyplot(plot0, clear_figure=True)
with col2:
    plot1 = (
        df.loc["Columnas"]
        .plot(kind="bar", title="Número de Columnas", color="red", edgecolor="black")
        .figure
    )
    st.pyplot(plot1, clear_figure=True)
