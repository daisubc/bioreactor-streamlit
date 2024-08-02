import streamlit as st
import numpy as np
from pandas import DataFrame

if "data" not in st.session_state:
    simulation_inited = False
else:
    simulation_inited = True


def download_data():
    if "data" in st.session_state and st.session_state.auto_refresh:
        return st.session_state["data"].to_csv().encode("utf-8")
    else:
        return DataFrame().to_csv().encode("utf-8")


def alert_user(Glc, Gln):

    if Glc > st.session_state.alarms[0]:
        st.toast(
            "Glucose concentration exceeds {}".format(st.session_state.alarms[0]),
            icon="🚨",
        )

    if Gln > st.session_state.alarms[1]:
        st.toast(
            "Glutamine concentration exceeds {}".format(st.session_state.alarms[1]),
            icon="🚨",
        )


def toggle_simulation():
    if st.session_state.running_toggle:
        st.session_state.auto_refresh = True
    else:
        st.session_state.auto_refresh = False


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
        st.toggle(
            "Run Simulation",
            value=st.session_state.auto_refresh,
            key="running_toggle",
            on_change=toggle_simulation,
        )

        if "data" in st.session_state:
            st.markdown(
                f"Simulation Time: *{st.session_state['data']['t'].iloc[-1]}* h"
            )

        app_dt = st.select_slider(
            "Select Simulation Step Time",
            options=[
                "1 hour",
                "2 hours",
                "3 hours",
                "4 hours",
                "5 hours",
            ],
        )

        st.session_state.app_dt = int(app_dt[0])

        speed = st.select_slider("Simulation Speed:", options=["1x", "2x", "3x"])
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
        st.subheader("**Initial Conditions**")
        col1, col2 = st.columns(2)
        with col1:
            with st.container():
                X_0 = st.number_input(
                    "$X_0$ (cells/mL)",
                    value=2.0e5,
                    min_value=1.0e5,
                    max_value=1.0e6,
                    format="%0.1e",
                    disabled=st.session_state.auto_refresh,
                )
                Glc_0 = st.number_input(
                    "$Glc_0$ (mM)",
                    value=35,
                    min_value=0,
                    max_value=60,
                    disabled=st.session_state.auto_refresh,
                )
                Lac = st.number_input(
                    "$Lac$ (mM)",
                    value=0,
                    min_value=0,
                    max_value=60,
                    disabled=st.session_state.auto_refresh,
                )
        with col2:
            with st.container():
                P_0 = st.number_input(
                    "$P_0$ (mg/mL)",
                    value=0,
                    min_value=0,
                    max_value=400,
                    disabled=st.session_state.auto_refresh,
                )
                Gln_0 = st.number_input(
                    "$Gln_0$ (mM)",
                    value=4,
                    min_value=0,
                    max_value=10,
                    disabled=st.session_state.auto_refresh,
                )
                Amm = st.number_input(
                    "$Amm$ (mM)",
                    value=0,
                    min_value=0,
                    max_value=100,
                    disabled=st.session_state.auto_refresh,
                )

        V = st.number_input(
            "$Volume$ (mL)",
            value=1000,
            min_value=0,
            max_value=10000,
            disabled=st.session_state.auto_refresh,
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
            "Glucose Dosing Time (h)", options=np.arange(0, 251, 25), value=(175, 225)
        )

        t0_gln, tn_gln = st.select_slider(
            "Glutamine Dosing Time (h)", options=np.arange(0, 251, 25), value=(175, 225)
        )

        st.subheader("**Alarms**")
        col5, col6 = st.columns(2)
        max_Glc = col5.number_input(
            "Max Glc (mM)", value=60.0, min_value=0.0, max_value=100.0
        )

        max_Gln = col6.number_input(
            "Max Gln (mM)", value=10.0, min_value=0.0, max_value=100.0
        )

        st.session_state.initial_vals = [Glc_0, Gln_0, X_0, P_0, Amm, Lac, V]
        st.session_state.flows = [F_Glc, F_Gln]
        st.session_state.t_glc = (t0_glc, tn_glc)
        st.session_state.t_gln = (t0_gln, tn_gln)
        st.session_state.alarms = [max_Glc, max_Gln]
