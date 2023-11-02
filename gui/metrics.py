import streamlit as st
from millify import millify


def mk_metrics():
    st.divider()

    if "data" not in st.session_state:
        st.caption(
            "*The bioreactor is not running. Read the instructions below and click on 'Run Simulation' to begin.*"
        )
    else:
        st.markdown(
            f"##### Bioreactor Process Monitoring Dashboard. $t={st.session_state['data']['t'].iloc[-1]}$ hrs"
        )

    col1, col2, col3 = st.columns(3)

    if "data" not in st.session_state:
        col1.metric("$X_v$", None)
        col1.markdown("Viable cell concentration in cells per milliliter")
        col2.metric("$P$", None)
        col2.markdown("Product concentration in micrograms per milliliter")
        col3.metric("$F_{Glc}$", None)
        col3.markdown("Flowrate of glucose into the reactor")
        col1.metric("$Glc$", None)
        col1.markdown("Glucose concentration in millimolar")
        col2.metric("$Gln$", None)
        col2.markdown("Glutamine concentration in millimolar")
        col3.metric("$F_{Gln}$", None)
        col3.markdown("Flowrate of glutamine into the reactor")
    else:
        data = st.session_state["data"]
        values = data.iloc[-1]

        if data.shape[0] > 1:
            delta = data.iloc[-1] - data.iloc[-2]
        else:
            delta = data.iloc[-1] - data.iloc[-1]

        col1.metric(
            "$X_v$",
            "{} {}".format(millify(values["X"]), "Cells/mL"),
            delta="{} {}".format(millify(delta["X"]), "Cells/mL"),
            help="Viable cell concentration in cells per milliliter",
        )
        col1.markdown("Viable cell concentration in cells per milliliter")
        col2.metric(
            "$P$",
            "{} {}".format(millify(values["P"]), "mg/mL"),
            delta="{} {}".format(millify(delta["P"]), "mg/mL"),
        )
        col2.markdown("Product concentration in milligrams per milliliter")
        col3.metric(
            "$F_{Glc}$",
            "{} {}".format(millify(values["F_Glc"]), "L/h"),
            delta="{} {}".format(millify(delta["F_Glc"]), "L/h"),
        )
        col3.markdown("Flowrate of glucose into the reactor")
        col1.metric(
            "$Glc$",
            "{} {}".format(millify(values["Glc"]), "mM"),
            delta="{} {}".format(millify(delta["Glc"]), "mM"),
        )
        col1.markdown("Glucose concentration in millimolar")
        col2.metric(
            "$Gln$",
            "{} {}".format(millify(values["Gln"]), "mM"),
            delta="{} {}".format(millify(delta["Gln"]), "mM"),
        )
        col2.markdown("Glutamine concentration in millimolar")
        col3.metric(
            "$F_{Gln}$",
            "{} {}".format(millify(values["F_Gln"]), "L/h"),
            delta="{} {}".format(millify(delta["F_Gln"]), "L/h"),
        )
        col3.markdown("Flowrate of glutamine into the reactor")
