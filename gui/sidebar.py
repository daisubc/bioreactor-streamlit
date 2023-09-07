import streamlit as st
import numpy as np

def mk_sidebar(
        title="Default Title", 
        caption="Default Caption"
               ):
    
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
        st.session_state.auto_refresh = st.checkbox('Run Simulation')

        speed = st.select_slider("Speed Equals:", options=['1x', '2x', '3x'])
        st.session_state.sleep_time = 0.1 / int(speed[0])

    with st.expander("Control Panel"):
        st.subheader("**Initial Concentrations**")
        col1, col2 = st.columns(2)
        with col1:
            with st.container():
                Glc_0 = st.number_input('$Glc_0$ (mM)', value=35, min_value=0, max_value=60)
        with col2:
            with st.container():
                Gln_0 = st.number_input('$Gln_0$ (mM)', value=4, min_value=0, max_value=10)
        
        st.subheader("**Feed Flowrates**")
        col3, col4 = st.columns(2)
        with col3:
            F_Glc = st.number_input('$F_{Glc}$ (L/h)', value=0.0, min_value=0.0, max_value=5.0)
        with col4:
            F_Gln = st.number_input(
                '$F_{Gln}$ (L/h)', value=0.0, min_value=0.0, max_value=5.0)

        st.subheader("**Dosing Times**")
        t0_glc, tn_glc = st.select_slider(
                'Glucose Dosing Time (h)',
                options=np.arange(0, 250, 25),
                value=(175, 225))
        
        t0_gln, tn_gln = st.select_slider(
                'Glutamine Dosing Time (h)',
                options=np.arange(0, 250, 25),
                value=(175, 225))
        
        st.session_state.initial_vals = [Glc_0, Gln_0]
        st.session_state.flows = [F_Glc, F_Gln]
        st.session_state.t_glc = (t0_glc, tn_glc)
        st.session_state.t_gln = (t0_gln, tn_gln)