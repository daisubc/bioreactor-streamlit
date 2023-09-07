import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-poster')

def write_XP_graph():

    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    fig.tight_layout()

    if "data" in st.session_state:
        p_data = [st.session_state['data']['P'][i]
                for i in range(len(st.session_state['data']['P']))]
        x_data = [st.session_state['data']['X'][i]
                for i in range(len(st.session_state['data']['X']))]
        t_data = [st.session_state['data']['t'][i]
                for i in range(len(st.session_state['data']['t']))]

        ax.plot(t_data, x_data, '--or', label="Xv (c/mL)")
        ax2.plot(t_data, p_data, '--ob', label="Product")

        ax.legend(loc="upper left")
        ax2.legend(loc="lower left")

    color = 'tab:red'
    ax.set_xlabel('Time (h)')
    ax.set_ylabel('Xv (c/mL)', color=color)

    ax.set_ylim(bottom=0)

    color = 'tab:blue'
    ax2.set_ylabel("P (ug/mL)")
    ax2.tick_params(axis='y', labelcolor=color)

    st.pyplot(fig)


def write_nutrients_graph():

    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    fig.tight_layout()

    if "data" in st.session_state:
        lac_data = [st.session_state['data']['Lac'][i]
                for i in range(len(st.session_state['data']['Lac']))]
        glc_data = [st.session_state['data']['Glc'][i]
                for i in range(len(st.session_state['data']['Glc']))]
        gln_data = [st.session_state['data']['Gln'][i]
                for i in range(len(st.session_state['data']['Gln']))]
        amm_data = [st.session_state['data']['Amm'][i]
                for i in range(len(st.session_state['data']['Amm']))]
        t_data = [st.session_state['data']['t'][i]
                for i in range(len(st.session_state['data']['t']))]
        
        ax.plot(t_data, glc_data, color="red", label="Glucose")
        ax.plot(t_data, lac_data, color="blue", label="Lactate")
        ax2.plot(t_data, gln_data, color="green", label="Glutamine")
        ax2.plot(t_data, amm_data, color="cyan", label="Ammonium")

        ax.legend(loc="upper left")
        ax2.legend(loc="lower left")

    ax.set_xlabel('Time (h)')
    ax.set_ylabel('Glc, Lac (mM)')
    ax.set_ylim(bottom=0)

    ax2.set_ylabel("Gln, Amm (mM)")
    ax2.tick_params(axis='y')
    ax2.set_ylim(bottom=0)

    fig.tight_layout()


    st.pyplot(fig)

def write_volume_graph():

    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    fig.tight_layout()

    if "data" in st.session_state:
        v_data = [st.session_state['data']['V'][i] for i in range(len(st.session_state['data']['V']))]
        f_glc_data = [st.session_state['data']['F_Glc'][i] for i in range(len(st.session_state['data']['F_Glc']))]
        f_gln_data = [st.session_state['data']['F_Gln'][i] for i in range(len(st.session_state['data']['F_Gln']))]
        t_data = [st.session_state['data']['t'][i] for i in range(len(st.session_state['data']['t']))]

        ax.plot(t_data, v_data, color="red", label="Volume")
        ax2.plot(t_data, f_glc_data, color="blue", label="F_Glc")
        ax2.plot(t_data, f_gln_data, color="green", label="F_Gln")
        ax.legend(loc="upper left")
        ax2.legend(loc="lower left")

    ax.set_xlabel('Time (h)')
    ax.set_ylabel('Volume (mL)')

    ax2.set_ylabel("Flow (L/h)")
    ax2.set_ylim(bottom=0)

    st.pyplot(fig)