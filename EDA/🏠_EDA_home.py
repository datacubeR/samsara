import pandas as pd
import streamlit as st
from pages.utils import create_histogram, import_data, summary_data

st.set_page_config(layout="wide")
st.markdown(
    """
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """,
    unsafe_allow_html=True,
)
st.markdown("# EDA Samsara")

if "EXCLUDE_COLUMNS" not in st.session_state:
    st.session_state.EXCLUDE_COLUMNS = ["not_null", "not_null_perc"]
if "df_dict" not in st.session_state:
    st.session_state.df_dict = import_data()

col1, col2 = st.columns(2)
df = pd.DataFrame(
    {name: data.shape for name, data in st.session_state.df_dict.items()},
    index=["Filas", "Columnas"],
)

with col1:
    plot0 = (
        df.loc["Filas"]
        .plot(
            kind="bar",
            title="Número de Filas",
            color="green",
            edgecolor="black",
        )
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
