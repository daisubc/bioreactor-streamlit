import streamlit as st
from time import sleep
import pandas as pd
import warnings

from gui.sidebar import mk_sidebar, alert_user, BOLUS_TIMES, DEADBAND
from gui.instructions import render_instructions
from gui.metrics import mk_metrics
from gui.graph import write_XP_graph, write_nutrients_graph, write_volume_graph

from model.run import init_sim, gen, param
from millify import millify

# Un-comment for Profiling
# from pathlib import Path
# from pyinstrument import Profiler

# profiler = Profiler()
# profiler.start()

# App Configuration

st.set_page_config(page_title="BioReactorSim", page_icon=":joystick:", layout="wide")

warnings.filterwarnings(
    "ignore", message="I don't know how to infer vegalite type from 'empty'"
)

# Constants

T_MAX = 250
N = 25

# Some initial values

GLC_F = 2500
Glc_F = GLC_F  # mM
Gln_F = 100  # mM
F_Glc = 0  # L / h
F_Gln = 0  # L / h
F_B = 0  # L / h

if not "auto_refresh" in st.session_state:
    st.session_state.auto_refresh = False

if not "sleep_time" in st.session_state:
    st.session_state.sleep_time = 0.1

# Create Sidebar

with st.sidebar:
    mk_sidebar(
        title="Controls",
        caption="Use these widgets to manipulate the simulation and the bioprocess!",
    )

# initialize during first run
if "data" not in st.session_state and st.session_state.auto_refresh:
    # Integration parameters
    t_max = T_MAX  # h

    [Glc_0, Gln_0, X_0, P_0, Amm, Lac, V_0] = st.session_state.initial_vals

    res = init_sim(
        Glc_0=Glc_0,
        Gln_0=Gln_0,
        X_0=X_0,
        P_0=P_0,
        V_0=V_0,
        Lac_0=Lac,
        Amm_0=Amm,
        params=st.session_state.param_df.to_dict(),
    )
    st.session_state["data"] = (
        pd.DataFrame([res]).astype("float64").set_index("t", drop=False)
    )


# Title
st.title("CHO Cell Bioreactor Simulator")
st.subheader("An interactive bioprocess simulation")

mk_metrics()

tab1, tab2 = st.tabs(
    [
        ":question: Instructions",
        ":joystick: Simulation",
    ]
)

if "data" in st.session_state:
    data = st.session_state.data
else:
    data = pd.DataFrame(
        columns=[
            "X",
            "P",
            "t",
            "Lac",
            "Glc",
            "Gln",
            "Amm",
            "V",
            "F_Gln",
            "F_Glc",
        ]
    )

# Center Visual
with tab1:
    render_instructions(param)

with tab2:
    st.subheader("Cells, Products & Process Volume")
    cells, products = write_XP_graph(data)
    volume, feed_flows = write_volume_graph(data)
    left, middle, right = st.columns(3)
    Xchart = left.altair_chart(cells, use_container_width=True)
    Pchart = middle.altair_chart(products, use_container_width=True)
    volume_chart = right.altair_chart(volume, use_container_width=True)

    # FIXME: Hacky fix to resolve https://discuss.streamlit.io/t/tool-tips-in-fullscreen-mode-for-charts/6800/8
    st.markdown(
        "<style>#vg-tooltip-element{z-index: 1000051}</style>", unsafe_allow_html=True
    )

    st.subheader("Nutrients, Metabolites & Feed Volumes")

    chart1, chart2 = write_nutrients_graph(data)
    left, middle, right = st.columns(3)
    glc_lac_chart = left.altair_chart(chart1, use_container_width=True)
    gln_amm_chart = middle.altair_chart(chart2, use_container_width=True)
    feed_chart = right.altair_chart(feed_flows, use_container_width=True)

if st.session_state.auto_refresh:
    data = st.session_state["data"]

    # Get Control Values from Front-end
    if st.session_state.control_mode == "Bolus Feed":

        app_dt = st.session_state.app_dt
        for i, _ in enumerate(BOLUS_TIMES):
            if data["t"].iloc[-1] <= BOLUS_TIMES[i] < data["t"].iloc[-1] + app_dt:
                F_Glc = st.session_state.bolus_feeds[i] / 1000
                Glc_F = GLC_F * 10
                break
            else:
                F_Glc = 0
                Glc_F = GLC_F

    elif st.session_state.control_mode == "Bang Control":

        Glc_DB, Gln_DB = st.session_state.DB

        if data["Glc"].iloc[-1] + Glc_DB < st.session_state.SP[0]:
            F_Glc = st.session_state.flows[0]
        else:
            F_Glc = 0

        if data["Gln"].iloc[-1] + Glc_DB < st.session_state.SP[1]:
            F_Gln = st.session_state.flows[1]
        else:
            F_Gln = 0
    else:
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

    # Start Calculation
    try:
        res_n = next(
            gen(
                data.iloc[-1],
                Glc_F,
                Gln_F,
                F_Glc,
                F_Gln,
                F_B,
                dt=st.session_state.app_dt,
            )
        )
        df_n = (
            pd.DataFrame()
            .from_dict([res_n])
            .astype("float64")
            .set_index("t", drop=False)
        )

        df_XP = (
            pd.DataFrame([{"t": res_n["t"], "X": res_n["X"], "P": res_n["P"]}])
            .astype("float64")
            .set_index("t", drop=False)
        )

        df_nutrients = (
            pd.DataFrame(
                [
                    {
                        "t": res_n["t"],
                        "Lac": res_n["Lac"],
                        "Glc": res_n["Glc"],
                        "Gln": res_n["Gln"],
                        "Amm": res_n["Amm"],
                    }
                ]
            )
            .astype("float64")
            .set_index("t", drop=False)
        )

        df_feed_volume = (
            pd.DataFrame(
                [
                    {
                        "t": res_n["t"],
                        "V": res_n["V"],
                        "F_Gln": res_n["F_Gln"],
                        "F_Glc": res_n["F_Glc"],
                    }
                ]
            )
            .astype("float64")
            .set_index("t", drop=False)
        )

        Xchart.add_rows(df_XP)
        Pchart.add_rows(df_XP)

        glc_lac_chart.add_rows(
            df_nutrients[["t", "Glc", "Lac"]].melt(
                id_vars="t",
                value_vars=["Glc", "Lac"],
                var_name="Nutrient",
                value_name="Value",
            )
        )

        gln_amm_chart.add_rows(
            df_nutrients[["t", "Gln", "Amm"]].melt(
                id_vars="t",
                value_vars=["Gln", "Amm"],
                var_name="Nutrient",
                value_name="Value",
            )
        )

        volume_chart.add_rows(df_feed_volume)
        feed_chart.add_rows(
            df_feed_volume[["t", "F_Gln", "F_Glc"]].melt(
                id_vars="t",
                value_vars=["F_Gln", "F_Glc"],
                var_name="Nutrient",
                value_name="Value",
            )
        )

        st.session_state["data"] = pd.concat(
            [data, df_n],
        )

        alert_user(data["Glc"].iloc[-1], data["Gln"].iloc[-1])

        # profiler.stop()
        # html_file = profiler.output_html()
        # file = Path("profile.html")
        # file.write_text(html_file, encoding="utf-8")

    except StopIteration:
        st.toast("Simulation Complete! :partying_face:")
        st.toast(
            "Maximum cell concentration of {} achieved at {} hours".format(
                millify(max(data["X"]), precision=2), data["X"].idxmax()
            )
        )
        st.session_state.auto_refresh = False
    else:
        sleep(st.session_state.sleep_time)
        # st.session_state['data']['i'] += 1
        st.rerun()
