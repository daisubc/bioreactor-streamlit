import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import altair as alt

plt.style.use("seaborn-poster")


def get_data(columns):
    if "data" in st.session_state:
        return st.session_state["data"][columns]
    else:
        return pd.DataFrame(columns=columns)


def write_XP_graph():
    data = get_data(["t", "X", "P"])

    # First chart for Glc and Lac
    chart1 = alt.layer(
        alt.Chart(data)
        .mark_line(color="black")
        .encode(x=alt.X("t:Q", title="Time (h)"), y=alt.Y("X:Q", title="Cells (c/mL)")),
    )

    # Second chart for Gln and Amm
    chart2 = alt.layer(
        alt.Chart(data)
        .mark_line(color="blue")
        .encode(
            x=alt.X("t:Q", title="Time (h)"), y=alt.Y("P:Q", title="Product (ug/mL)")
        ),
    )

    left, right = st.columns(2)
    left.altair_chart(chart1, use_container_width=True)
    right.altair_chart(chart2, use_container_width=True)


def write_nutrients_graph():
    data = get_data(["t", "Lac", "Glc", "Gln", "Amm"])

    # First chart for Glc and Lac
    chart1 = alt.Chart(data).mark_line(color="blue").encode(
        x=alt.X("t:Q", title="Time (h)"), y=alt.Y("Glc:Q", title="Glc (mM)")
    ) + alt.Chart(data).mark_line(color="lime").encode(
        x=alt.X("t:Q", title="Time (h)"), y=alt.Y("Lac:Q", title="Lac (mM)")
    )

    # Second chart for Gln and Amm
    chart2 = alt.Chart(data).mark_line(color="red").encode(
        x=alt.X("t:Q", title="Time (h)"), y=alt.Y("Gln:Q", title="Gln (mM)")
    ) + alt.Chart(data).mark_line(color="orange").encode(
        x=alt.X("t:Q", title="Time (h)"), y=alt.Y("Amm:Q", title="Amm (mM)")
    )

    # Display the charts in Streamlit
    left, right = st.columns(2)
    left.altair_chart(chart1, use_container_width=True)
    right.altair_chart(chart2, use_container_width=True)


def write_volume_graph():
    data = get_data(["t", "V", "F_Gln", "F_Glc"])

    # First chart for Glc and Lac
    chart2 = alt.Chart(data).mark_line(color="blue").encode(
        x=alt.X("t:Q", title="Time (h)"), y=alt.Y("F_Gln:Q", title="F_Gln (L/h)")
    ) + alt.Chart(data).mark_line(color="red").encode(
        x=alt.X("t:Q", title="Time (h)"), y=alt.Y("F_Glc:Q", title="F_Glc (L/h)")
    )

    # Second chart for Gln and Amm
    chart1 = (
        alt.Chart(data)
        .mark_line(color="purple")
        .encode(
            x=alt.X("t:Q", title="Time (h)"),
            y=alt.Y("V:Q", title="Volume (L)"),
        )
    )

    # Display the charts in Streamlit
    left, right = st.columns(2)
    left.altair_chart(chart1, use_container_width=True)
    right.altair_chart(chart2, use_container_width=True)
