import pandas as pd
import streamlit as st
from pages.utils import import_data

st.set_page_config(layout="wide")
st.markdown("# EDA Samsara")

if "EXCLUDE_COLUMNS" not in st.session_state:
    st.session_state.EXCLUDE_COLUMNS = ["not_null", "not_null_perc"]
if "df_dict" not in st.session_state:
    st.session_state.df_dict = import_data()


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
        .plot(
            kind="bar",
            title="Número de Columnas",
            color="red",
            edgecolor="black",
        )
        .figure
    )
    st.pyplot(plot1, clear_figure=True)


col1, col2, col3, col4, col5 = st.columns(5)
cols = [col1, col2, col3, col4, col5]
colors = ["green", "orange", "yellow", "brown", "magenta"]
for col, evento, color in zip(cols, st.session_state.df_dict.keys(), colors):
    with col:
        summary_data(evento)
        create_histogram(evento, color)
