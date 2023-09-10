import streamlit as st
from millify import millify


def mk_metrics():
    col1, col2, col3 = st.columns(3)

    if "data" not in st.session_state:
        col1.metric(
            "$X_v$", None, help="Viable cell concentration in cells per milliliter"
        )
        col2.metric(
            "$P$", None, help="Product concentration in micrograms per milliliter"
        )
        col3.metric(
            "$F_{Glc}$",
            None,
            help="Flowrate of glucose into the reactor in litres per hour",
        )
        col1.metric("$Glc$", None, help="Glucose concentration in millimolar")
        col2.metric("$Gln$", None, help="Glutamine concentration in millimolar")
        col3.metric(
            "$F_{Gln}$",
            None,
            help="Flowrate of glutamine into the reactor in litres per hour",
        )
    else:
        data = st.session_state["data"]
        values = data.iloc[-1]

        if data.shape[0] > 1:
            delta = data.iloc[-1] - data.iloc[-2]
        else:
            delta = data.iloc[-1] - data.iloc[-1]

        col1.metric(
            "$X_v$",
            "{} {}".format(millify(values["X"]), "c/mL"),
            delta="{} {}".format(millify(delta["X"]), "c/mL"),
            help="Viable cell concentration in cells per milliliter",
        )
        col2.metric(
            "$P$",
            "{} {}".format(millify(values["P"]), "ug/mL"),
            delta="{} {}".format(millify(delta["P"]), "ug/mL"),
            help="Product concentration in micrograms per milliliter",
        )
        col3.metric(
            "$F_{Glc}$",
            "{} {}".format(millify(values["F_Glc"]), "L/h"),
            delta="{} {}".format(millify(delta["F_Glc"]), "L/h"),
            help="Flowrate of glucose into the reactor in litres per hour",
        )
        col1.metric(
            "$Glc$",
            "{} {}".format(millify(values["Glc"]), "mM"),
            delta="{} {}".format(millify(delta["Glc"]), "mM"),
            help="Glucose concentration in millimolar",
        )
        col2.metric(
            "$Gln$",
            "{} {}".format(millify(values["Gln"]), "mM"),
            delta="{} {}".format(millify(delta["Gln"]), "mM"),
            help="Glutamine concentration in millimolar",
        )
        col3.metric(
            "$F_{Gln}$",
            "{} {}".format(millify(values["F_Gln"]), "L/h"),
            delta="{} {}".format(millify(delta["F_Gln"]), "L/h"),
            help="Flowrate of glutamine into the reactor in litres per hour",
        )
