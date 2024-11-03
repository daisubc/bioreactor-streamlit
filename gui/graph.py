import altair as alt

## DO NOT CACHE THE CHARTS


def create_layered_graph(data, color, y_axis, title):
    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection_point(
        nearest=True,
        on="mouseover",
        encodings=["x"],
        empty=False,
    )

    line = (
        alt.Chart(data)
        .mark_line(color=color)
        .encode(
            x=alt.X("t:Q"),
            y=alt.Y((y_axis + ":Q")),
        )
    )

    # First chart for Glc and Lac
    chart = alt.layer(
        line,
        # Transparent selectors across the chart. This is what tells us
        # the x-value of the cursor
        alt.Chart(data)
        .mark_point()
        .encode(
            x=alt.X("t:Q", title="Time (h)"),
            y=alt.Y((y_axis + ":Q"), title=title),
            tooltip=[
                alt.Tooltip("t", title="Time (h)", type="quantitative", format=".1f"),
                alt.Tooltip(y_axis, title=title, type="quantitative", format=".1f"),
            ],
            opacity=alt.value(0),
        )
        .add_params(nearest),
        # Draw a rule at the location of the selection
        alt.Chart(data)
        .mark_rule(color=color)
        .encode(
            x=alt.X("t:Q"),
        )
        .transform_filter(nearest),
        line.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        ),
    )

    return chart


def create_layered_graph_long(data_long, title, colors=None, domain=None):
    # Set default colors if none are provided
    if colors is None:
        colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

    # Automatically determine domain from data if not provided
    if domain is None:
        domain = (
            data_long[data_long.columns[1]].unique().tolist()
        )  # Assumes second column is categorical

    # Determine y-axis title and units based on the title
    if "Nutrient" in title:
        y_axis_title = "Nutrient Concentration (mM)"
    elif "Feed Flow" in title:
        y_axis_title = "Flow Rate (L/h)"
    else:
        y_axis_title = "Value"

    # Selection to highlight the nearest point on the x-axis
    nearest = alt.selection_point(
        nearest=True,
        on="mouseover",
        encodings=["x"],
        empty=False,
    )

    # Base line chart for each category
    line = (
        alt.Chart(data_long)
        .mark_line()
        .encode(
            x=alt.X("t:Q", title="Time (h)"),
            y=alt.Y("Value:Q", title=y_axis_title),
            color=alt.Color(
                data_long.columns[1] + ":N",
                scale=alt.Scale(range=colors, domain=domain),
                title=data_long.columns[1],
            ),
        )
    )

    # Pivot the data to create a format suitable for showing all variables in a single tooltip
    tooltip_data = (
        alt.Chart(data_long)
        .transform_pivot(
            data_long.columns[1],  # Pivot on the categorical variable
            value="Value",
            groupby=["t"],
        )
        .mark_rule()
        .encode(
            x="t:Q",
            opacity=alt.condition(nearest, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("t:Q", title="Time (h)"),
                *[alt.Tooltip(f"{var}:Q", title=var, format=".2f") for var in domain],
            ],
        )
        .add_params(nearest)
    )

    # Points on the line chart for highlighting the selection
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Layer line, tooltip, and points together
    chart = alt.layer(line, tooltip_data, points).properties(title=title)

    return chart


def write_XP_graph(data):
    data = data[["t", "X", "P"]]

    chart1 = create_layered_graph(data, "black", "X", "Cells (Cells/mL)")

    # Second chart for Gln and Amm
    chart2 = create_layered_graph(data, "blue", "P", "Product (mg/mL)")

    return chart1, chart2


def write_nutrients_graph(data):
    data = data[["t", "Lac", "Glc", "Gln", "Amm"]]

    data_long = data[["t", "Glc", "Lac"]].melt(
        id_vars="t", value_vars=["Glc", "Lac"], var_name="Nutrient", value_name="Value"
    )

    chart1 = create_layered_graph_long(
        data_long, "Nutrient", ["blue", "grey"], ["Glc", "Lac"]
    )

    # Second chart for Gln and Amm

    data_long = data[["t", "Gln", "Amm"]].melt(
        id_vars="t", value_vars=["Gln", "Amm"], var_name="Nutrient", value_name="Value"
    )

    chart2 = create_layered_graph_long(
        data_long, "Nutrient", ["orange", "red"], ["Gln", "Amm"]
    )

    # Display the charts in Streamlit
    return chart1, chart2


def write_volume_graph(data):
    data = data[["t", "V", "F_Gln", "F_Glc"]]

    data_long = data[["t", "F_Gln", "F_Glc"]].melt(
        id_vars="t",
        value_vars=["F_Glc", "F_Gln"],
        var_name="Feed Flow",
        value_name="Value",
    )

    chart2 = create_layered_graph_long(
        data_long, "Feed Flow", ["orange", "blue"], ["F_Gln", "F_Glc"]
    )

    # Second Chart for volume
    chart1 = create_layered_graph(data, "purple", "V", "Volume (mL)")

    # Display the charts in Streamlit
    return chart1, chart2
