import streamlit as st
from time import sleep
import pandas as pd

from gui.sidebar import mk_sidebar
from gui.instructions import render_instructions
from gui.metrics import mk_metrics
from gui.graph import write_XP_graph, write_nutrients_graph, write_volume_graph

from model.run import init_sim, gen, param


st.set_page_config(page_title="BioReactorSim", page_icon=":joystick:")

if not "auto_refresh" in st.session_state:
    st.session_state.auto_refresh = False

if not "sleep_time" in st.session_state:
    st.session_state.sleep_time = 0.1

with st.sidebar:
    mk_sidebar(
        title="Controls",
        caption="Use these widgets to manipulate the simulation and the bioprocess!",
    )

# initialize during first run
if "data" not in st.session_state and st.session_state.auto_refresh:
    # Integration parameters
    t_max = 250  # h
    N = 25  # points

    [Glc_0, Gln_0] = st.session_state.initial_vals

    res = init_sim(Glc_0=Glc_0, Gln_0=Gln_0)
    st.session_state["data"] = pd.DataFrame([res])

# Some initial values
Glc_F = 2500  # mM
Gln_F = 100
F_Glc = 0
F_Gln = 0
F_B = 0

st.title("CHO Cell Bioreactor Simulator")
st.subheader("An interactive bioprocess simulation")

mk_metrics()

tab1, tab2, tab3, tab4 = st.tabs(
    [
        ":question: Instructions",
        ":moneybag: Cells & Product",
        ":carrot: Substrate",
        ":alembic: Volume & Flows",
    ]
)

# Center Visual
with tab1:
    render_instructions(param)

with tab2:
    write_XP_graph()

with tab3:
    write_nutrients_graph()

with tab4:
    write_volume_graph()

if st.session_state.auto_refresh:
    data = st.session_state["data"]

    t0_glc, tn_glc = st.session_state.t_glc
    if t0_glc <= data["t"].iloc[-1] <= tn_glc:
        F_Glc = st.session_state.flows[0]
    else:
        F_Glc = 0

    t0_gln, tn_gln = st.session_state.t_gln
    if t0_gln <= data["t"].iloc[-1] <= tn_gln:
        F_Gln = st.session_state.flows[1]
    else:
        F_Gln = 0

    try:
        res_n = next(gen(data.iloc[-1], Glc_F, Gln_F, F_Glc, F_Gln, F_B))

        st.session_state["data"] = pd.concat(
            [data, pd.DataFrame([res_n])], ignore_index=True
        )
    except StopIteration:
        st.toast("Simulation Complete! :partying_face:")
        st.session_state.auto_refresh = False

    sleep(st.session_state.sleep_time)
    # st.session_state['data']['i'] += 1
    st.experimental_rerun()
