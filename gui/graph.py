import altair as alt

## DO NOT CACHE THE CHARTS


def write_XP_graph(data):
    data = data[["t", "X", "P"]]

    # First chart for Glc and Lac
    chart1 = alt.layer(
        alt.Chart(data)
        .mark_line(color="black")
        .encode(
            x=alt.X("t:Q", title="Time (h)"),
            y=alt.Y("X:Q", title="Cells (Cells/mL)"),
        ),
    )

    # Second chart for Gln and Amm
    chart2 = alt.layer(
        alt.Chart(data)
        .mark_line(color="blue")
        .encode(
            x=alt.X("t:Q", title="Time (h)"), y=alt.Y("P:Q", title="Product (mg/mL)")
        ),
    )

    return chart1, chart2


def write_nutrients_graph(data):
    data = data[["t", "Lac", "Glc", "Gln", "Amm"]]

    # First chart for Glc and Lac
    chart1 = alt.Chart(data).mark_line().encode(
        x=alt.X("t:Q", title="Time (h)"),
        y=alt.Y("Glc:Q", title="Glc (mM)"),
        color=alt.datum("Glc"),
    ) + alt.Chart(data).mark_line().encode(
        x=alt.X("t:Q", title="Time (h)"),
        y=alt.Y("Lac:Q", title="Lac (mM)"),
        color=alt.datum("Lac"),
    )

    # Second chart for Gln and Amm
    chart2 = alt.Chart(data).mark_line(color="red").encode(
        x=alt.X("t:Q", title="Time (h)"), y=alt.Y("Gln:Q", title="Gln (mM)")
    ) + alt.Chart(data).mark_line(color="orange").encode(
        x=alt.X("t:Q", title="Time (h)"), y=alt.Y("Amm:Q", title="Amm (mM)")
    )

    # Display the charts in Streamlit
    return chart1, chart2


def write_volume_graph(data):
    data = data[["t", "V", "F_Gln", "F_Glc"]]

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
    return chart1, chart2
