import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from pages.utils import create_heatmap_df, import_data

st.set_page_config(layout="wide")
if "EXCLUDE_COLUMNS" not in st.session_state:
    st.session_state.EXCLUDE_COLUMNS = ["not_null", "not_null_perc"]
if "df_dict" not in st.session_state:
    st.session_state.df_dict = import_data()


c1, c2 = st.columns(2)
resample = c1.selectbox("Seleccionar Resample:", [None, "W", "2W", "M"])

col1, col2, col3 = st.columns([4, 1, 4])
heatmap_df = create_heatmap_df(
    st.session_state.df_dict, ex_col=st.session_state.EXCLUDE_COLUMNS
)
heatmap_df_resample = create_heatmap_df(
    st.session_state.df_dict, ex_col=st.session_state.EXCLUDE_COLUMNS, resample=resample
)

col1.pyplot(
    heatmap_df.eq(0)
    .sum()
    .to_frame()
    .plot(
        kind="bar",
        legend=False,
        color="green",
        edgecolor="black",
        title="Valores Nulos en TS Original",
    )
    .figure
)
col3.pyplot(
    heatmap_df_resample.eq(0)
    .sum()
    .to_frame()
    .plot(
        kind="bar",
        legend=False,
        color="yellow",
        edgecolor="black",
        title="Valores Nulos en TS Resampleado",
    )
    .figure
)

fig = plt.figure(figsize=(20, 20))
sns.heatmap(heatmap_df)
plt.title("Número de valores no nulos por Día")
col1.pyplot(fig, clear_figure=True)

fig = plt.figure(figsize=(20, 20))
sns.heatmap(heatmap_df_resample)
plt.title("Número de valores no nulos por Día")
col3.pyplot(fig, clear_figure=True)


#     fig = plt.figure(figsize=(20, 20))
#     sns.heatmap(heatmap_df)
#     plt.title("Número de valores no nulos por Día")
#     st.pyplot(fig, clear_figure=True)
#
# with col2:
#     fig = plt.figure(figsize=(20, 20))
#     sns.heatmap(heatmap_df_week)
#     plt.title("Número de valores no nulos por Semana")
#     st.pyplot(fig, clear_figure=True)
