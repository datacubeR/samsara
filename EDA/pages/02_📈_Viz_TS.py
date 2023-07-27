import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from pages.utils import calculate_metrics, import_data

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


c1, c2, c3, c4 = st.columns(4)

with c1:
    event = st.selectbox("Seleccionar Evento:", st.session_state.df_dict.keys())

with c2:
    data = st.session_state.df_dict[event]
    max_perc = data.not_null_perc.pipe(np.floor).max()
    min_perc = data.not_null_perc.pipe(np.floor).min()
    perc_slider = st.slider(
        "% Mediciones Válidas", min_value=min_perc, max_value=max_perc
    )
data = data.query("not_null_perc >= @perc_slider")
ids = c3.selectbox(
    "Seleccionar por ID: ",
    data.index.unique(),
)
c4.metric(
    label="TSs Resultantes:",
    value=f"{data.index.nunique()}/{st.session_state.df_dict[event].shape[0]}",
)


col1, col2 = st.columns(2)
data = st.session_state.df_dict[event].query("index == @ids")
with col1:
    st.metric(
        label="Número de Mediciones Válidas",
        value=f"{data['not_null'].iat[0]}/{data.drop(columns = ['not_null', 'not_null_perc']).shape[1]}",
    )
with col2:
    st.metric(
        label="Porcentaje de Mediciones Válidas",
        value=f"{data['not_null_perc'].iat[0]:.2f}%",
    )

ts = data.drop(columns=st.session_state.EXCLUDE_COLUMNS).T
ts.index = pd.to_datetime(ts.index)
ts = ts.reset_index()
ts.columns = ["Fecha", "Value"]
fig, ax = plt.subplots()
ts.plot(
    kind="line",
    x="Fecha",
    y="Value",
    figsize=(20, 5),
    title=f"TS Original: Evento: {event} - IDpix: {ids}",
    rot=90,
    legend=False,
    ax=ax,
    color="red",
)
ts.plot(kind="scatter", x="Fecha", y="Value", ax=ax, color="blue", s=10)
st.pyplot(fig, clear_figure=True)


col1, col2, col3 = st.columns(3)
resample = col1.selectbox(
    "Seleccionar Resample:", ["None", "Weekly", "Bi-Weekly", "Monthly"]
)
if resample == "Weekly":
    ts = ts.resample("W", on="Fecha").mean().reset_index()
if resample == "Bi-Weekly":
    ts = ts.resample("2W", on="Fecha").mean().reset_index()
elif resample == "Monthly":
    ts = ts.resample("M", on="Fecha").mean().reset_index()


nn, nnp = calculate_metrics(ts)
with col2:
    st.metric(
        label="Número de Mediciones Válidas",
        value=f"{nn}/{len(ts)}",
    )
with col3:
    st.metric(
        label="Porcentaje de Mediciones Válidas",
        value=f"{nnp:.2f}%",
    )


fig, ax = plt.subplots()
ts.plot(
    kind="line",
    x="Fecha",
    y="Value",
    figsize=(20, 5),
    title=f"TS Resampleada: Evento: {event} - IDpix: {ids}",
    rot=90,
    legend=False,
    ax=ax,
    color="red",
)
ts.plot(kind="scatter", x="Fecha", y="Value", ax=ax, color="blue", s=10)
st.pyplot(fig, clear_figure=True)

col1, col2, col3 = st.columns(3)
interpolation = col1.selectbox(
    "Seleccionar Interpolación:", ["None", "linear", "time", "ff", "bf"]
)
if interpolation == "linear":
    ts = ts.set_index("Fecha").interpolate().reset_index()
if interpolation == "time":
    ts = ts.set_index("Fecha").interpolate(method="time").reset_index()
elif interpolation == "ff":
    ts = ts.set_index("Fecha").fillna(method="ffill").reset_index()
elif interpolation == "bf":
    ts = ts.set_index("Fecha").fillna(method="bfill").reset_index()

nn, nnp = calculate_metrics(ts)
with col2:
    st.metric(
        label="Número de Mediciones Válidas",
        value=f"{nn}/{len(ts)}",
    )
with col3:
    st.metric(
        label="Porcentaje de Mediciones Válidas",
        value=f"{nnp:.2f}%",
    )

fig, ax = plt.subplots()
ts.plot(
    kind="line",
    x="Fecha",
    y="Value",
    figsize=(20, 5),
    title=f"TS Resampleada: Evento: {event} - IDpix: {ids}",
    rot=90,
    legend=False,
    ax=ax,
    color="red",
)
ts.plot(kind="scatter", x="Fecha", y="Value", ax=ax, color="blue", s=10)
st.pyplot(fig, clear_figure=True)
