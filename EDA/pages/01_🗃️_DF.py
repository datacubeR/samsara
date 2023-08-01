import streamlit as st
from pages.utils import import_data

st.set_page_config(layout="wide")
st.markdown(
    """
        <style>
               .block-container {
                    padding-top: 2rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """,
    unsafe_allow_html=True,
)
st.markdown("# Comparador de Series de Tiempo")
if "EXCLUDE_COLUMNS" not in st.session_state:
    st.session_state.EXCLUDE_COLUMNS = ["not_null", "not_null_perc"]
if "df_dict" not in st.session_state:
    st.session_state.df_dict = import_data()

c1, c2, c3 = st.columns(3)

with c1:
    event = st.selectbox("Seleccionar Evento:", st.session_state.df_dict.keys())

st.dataframe(st.session_state.df_dict[event])
