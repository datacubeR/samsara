import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from pages.utils import index_to_week  # noqa


def create_heatmap_df(dict, ex_col, week=False):
    output_dict = {}

    for name, data in dict.items():
        output_dict[name] = data.drop(columns=ex_col).notnull().sum().astype(bool).T
        output_dict[name].name = name

    output = pd.concat(output_dict.values(), axis=1).fillna(False).sort_index()
    if week:
        output.index = index_to_week(output)
    return output


col1, col2 = st.columns(2)
heatmap_df = create_heatmap_df(
    st.session_state.df_dict, ex_col=st.session_state.EXCLUDE_COLUMNS
)
heatmap_df_week = create_heatmap_df(
    st.session_state.df_dict, ex_col=st.session_state.EXCLUDE_COLUMNS, week=True
)

with col1:
    fig = plt.figure(figsize=(20, 20))
    sns.heatmap(heatmap_df)
    plt.title("Número de valores no nulos por Día")
    st.pyplot(fig, clear_figure=True)

with col2:
    fig = plt.figure(figsize=(20, 20))
    sns.heatmap(heatmap_df_week)
    plt.title("Número de valores no nulos por Semana")
    st.pyplot(fig, clear_figure=True)
