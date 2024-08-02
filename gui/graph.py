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

    data_long = data[["t", "Glc", "Lac"]].melt(
        id_vars="t", value_vars=["Glc", "Lac"], var_name="Nutrient", value_name="Value"
    )

    # First chart for Glc and Lac
    chart1 = (
        alt.Chart(data_long)
        .mark_line()
        .encode(
            x=alt.X("t:Q", title="Time (h)"),
            y=alt.Y("Value:Q", title="Concentration (mM)"),
            color=alt.Color(
                "Nutrient:N",
                scale=alt.Scale(range=["blue", "grey"], domain=["Glc", "Lac"]),
            ),
        )
    )

    # Second chart for Gln and Amm

    data_long = data[["t", "Gln", "Amm"]].melt(
        id_vars="t", value_vars=["Gln", "Amm"], var_name="Nutrient", value_name="Value"
    )

    chart2 = (
        alt.Chart(data_long)
        .mark_line()
        .encode(
            x=alt.X("t:Q", title="Time (h)"),
            y=alt.Y("Value:Q", title="Concentration (mM)"),
            color=alt.Color(
                "Nutrient:N",
                scale=alt.Scale(range=["orange", "red"], domain=["Gln", "Amm"]),
            ),
        )
        .interactive()
    )

    # Display the charts in Streamlit
    return chart1, chart2


def write_volume_graph(data):
    data = data[["t", "V", "F_Gln", "F_Glc"]]

    data_long = data[["t", "F_Gln", "F_Glc"]].melt(
        id_vars="t",
        value_vars=["F_Glc", "F_Gln"],
        var_name="Nutrient",
        value_name="Value",
    )

    # First chart for Glc and Lac
    chart2 = (
        alt.Chart(data_long)
        .mark_line()
        .encode(
            x=alt.X("t:Q", title="Time (h)"),
            y=alt.Y("Value:Q", title="Flow (L/h)"),
            color=alt.Color(
                "Nutrient:N",
                scale=alt.Scale(range=["orange", "blue"], domain=["F_Gln", "F_Glc"]),
            ),
        )
    )

    # Second chart for Gln and Amm
    chart1 = (
        alt.Chart(data)
        .mark_line(color="purple")
        .encode(
            x=alt.X("t:Q", title="Time (h)"),
            y=alt.Y("V:Q", title="Volume (mL)"),
        )
    )

    # Display the charts in Streamlit
    return chart1, chart2
