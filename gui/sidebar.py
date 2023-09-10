import streamlit as st
import numpy as np
from pandas import DataFrame


def download_data():
    if "data" in st.session_state:
        return st.session_state["data"].to_csv().encode("utf-8")
    else:
        return DataFrame().to_csv().encode("utf-8")


def reset_sim():
    st.toast("Simulation Reset!")
    del st.session_state["data"]


def mk_sidebar(title="Default Title", caption="Default Caption"):
    """
    Title & Caption
    """
    st.title(title)
    st.caption(caption)

    """
    Simulation Controls 
    """
    with st.expander("Simulation Controls", expanded=True):
        """
        Speed Control
        """
        st.session_state.auto_refresh = st.toggle(
            "Run Simulation", key="running_toggle"
        )

        speed = st.select_slider("Speed Equals:", options=["1x", "2x", "3x"])
        st.session_state.sleep_time = 0.1 / int(speed[0])

        col1, col2 = st.columns(2)
        csv = download_data()
        col1.download_button(
            ":arrow_down: Download CSV",
            data=csv,
            mime="text/csv",
            file_name="simulation_data.csv",
            disabled=st.session_state.auto_refresh,
            help="Get data from simulation. Stop the simulation to enable.",
        )

        col2.button(
            "Reset Simulation",
            on_click=reset_sim,
            disabled=st.session_state.auto_refresh,
            use_container_width=True,
        )

    with st.expander("Control Panel"):
        st.subheader("**Initial Concentrations**")
        col1, col2 = st.columns(2)
        with col1:
            with st.container():
                Glc_0 = st.number_input(
                    "$Glc_0$ (mM)", value=35, min_value=0, max_value=60
                )
        with col2:
            with st.container():
                Gln_0 = st.number_input(
                    "$Gln_0$ (mM)", value=4, min_value=0, max_value=10
                )

        st.subheader("**Feed Flowrates**")
        col3, col4 = st.columns(2)
        with col3:
            F_Glc = st.number_input(
                "$F_{Glc}$ (L/h)", value=0.0, min_value=0.0, max_value=5.0
            )
        with col4:
            F_Gln = st.number_input(
                "$F_{Gln}$ (L/h)", value=0.0, min_value=0.0, max_value=5.0
            )

        st.subheader("**Dosing Times**")
        t0_glc, tn_glc = st.select_slider(
            "Glucose Dosing Time (h)", options=np.arange(0, 250, 25), value=(175, 225)
        )

        t0_gln, tn_gln = st.select_slider(
            "Glutamine Dosing Time (h)", options=np.arange(0, 250, 25), value=(175, 225)
        )

        st.session_state.initial_vals = [Glc_0, Gln_0]
        st.session_state.flows = [F_Glc, F_Gln]
        st.session_state.t_glc = (t0_glc, tn_glc)
        st.session_state.t_gln = (t0_gln, tn_gln)
