import numpy as np
import pandas as pd
import streamlit as st
from pages.utils import import_data

if "EXCLUDE_COLUMNS" not in st.session_state:
    st.session_state.EXCLUDE_COLUMNS = ["not_null", "not_null_perc"]
if "df_dict" not in st.session_state:
    st.session_state.df_dict = import_data()


c1, c2 = st.columns(2)

with c1:
    event = st.selectbox("Seleccionar Evento:", st.session_state.df_dict.keys())
    data = st.session_state.df_dict[event]
    max_perc = data.not_null_perc.pipe(np.floor).max()
    min_perc = data.not_null_perc.pipe(np.floor).min()
    perc_slider = st.slider(
        "% Valores No Nulos Mínimo", min_value=min_perc, max_value=max_perc
    )

interpolation = c2.selectbox(
    "Seleccionar Interpolación:", ["None", "linear", "time", "ff", "bf"]
)

data = data.query("not_null_perc >= @perc_slider")

col1, col2 = st.columns(2)
col2.metric(
    label="Número TS: ",
    value=f"{data.index.nunique()}",
)
ids = col1.selectbox(
    "Seleccionar por ID: ",
    data.index.unique(),
)

data = st.session_state.df_dict[event].query("index == @ids")
col1, col2 = st.columns(2)
with col1:
    st.metric(
        label="Número de Eventos No Nulos",
        value=f"{data['not_null'].iat[0]}/{data.shape[1]}",
    )
with col2:
    st.metric(
        label="Porcentaje de Eventos No Nulos",
        value=f"{data['not_null_perc'].iat[0]:.2f}%",
    )

ts = data.drop(columns=st.session_state.EXCLUDE_COLUMNS).T
ts.index = pd.to_datetime(ts.index)
if interpolation == "linear":
    ts = ts.interpolate()
if interpolation == "time":
    ts = ts.interpolate(method="time")
elif interpolation == "ff":
    ts = ts.fillna(method="ffill")
elif interpolation == "bf":
    ts = ts.fillna(method="bfill")
st.pyplot(
    ts.plot(
        figsize=(20, 5),
        title=f"Evento: {event} - IDpix: {ids}",
        rot=90,
        legend=False,
    ).figure
)
