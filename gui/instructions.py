import streamlit as st
from pandas import DataFrame


def render_instructions(params):
    col1, col2 = st.columns(2)
    col1.markdown(
        """
        ### Instructions
                  
        The simulation is for CHO cells, _X_ secreting a recombinant protein product, _P_. Manipulate the initial concentrations of substrate for batch mode operation, 
        and test operating the reactor in fed-batch to yield optimal results.
                  
        To run the simulation, check the "Run Simulation" box. You can uncheck the box to pause the simulation. Additionally, you can adjust the speed of the simulation by
        dragging the slider to the right. 
    """
    )

    col2.markdown(
        """
        | Abbreviation | Definition                |
        |--------------|---------------------------|
        |     **X**    | Viable Cell Concentration |
        |     **P**    | Product                   |
        |    **Glc**   | Glucose                   |
        |    **Gln**   | Glutamine                 |
        |    **Amm**   | Ammonium                  |
        |    **PR**    | Production Rate           |
        |    **UR**    | Uptake Rate               |
    """
    )

    st.markdown(
        """
        ##### Simulation Controls
        Choose initial concentrations of $Glc_0$ and $Gln_0$ **before** starting the simulation. To operate in fed-batch, increase the feed flowrates $F_{Glc}$ and $F_{Gln}$.  
        
        For time controlled dosing, the feed will start when _t_ is within the defined dosing times. To manually control the dosing, select the dosing time between $ 0 < t < 225 $ and change $F_{Glc}$ and $F_{Gln}$ as desired.
        You can check that your substrate is being added in the *Volume & Flows* view.
    """
    )

    _, mid, _ = st.columns([1, 3, 1])
    mid.info(
        "Be attentive to the concentrations of your substrate. *Glc* should not exceed 60mM at any time. *Gln* should not exceed 10mM at any time.",
        icon="🚨",
    )

    # Equation & Constants Section
    st.markdown("#### Equations & Kinetic Constants")
    st.markdown("The following table shows the kinetic constants for the simulation.")
    df = DataFrame.from_dict(params, orient="index")
    df = df.rename(columns={0: "Values"})
    df["Units"] = [
        "1/h",
        "mM",
        "mM",
        "c/mmol",
        "mmol/c*h",
        "mM*mL/c*h",
        "mM",
        "M/M",
        "M/M",
        "ug/c",
        "ug/c*h",
        "mM",
        "mM",
        "mM",
        "mM",
        "mM",
    ]
    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "Values": st.column_config.NumberColumn(
                help="The value of the given parameter", format="%.2e"
            )
        },
    )

    st.markdown(
        """
        The growth of cells $\mu$ is given by the following equation:
    """
    )

    st.latex(
        r"""
        \mu = (\frac{\mu_{max}*Glc}{K_{s, Glc} + Glc})(\frac{0.5K_{s, Glc}+Gln}{K_{s, Gln} + Gln})(\frac{K_{l1,Amm}}{K_{l1,Amm} + Amm})(\frac{K_{l1, Lac}}{K_{l1, Lac} + Lac})
    """
    )

    st.markdown(
        """
        The cell death, $k_D$ can be expressed as:
    """
    )

    st.latex(
        r"""
        \begin{dcases}
        k_D = 0.05*(1-\frac{K_{l2, Amm}}{K_{l2, Amm} + Amm}) + 0.05(\frac{K_{l2, Lac}}{K_{l2, Lac} + Lac}) &\text{if } Glc > 0 \\
        k_D = 0.1 &\text{if } Glc = 0
        \end{dcases}
    """
    )

    st.markdown(
        """
        The glucose uptake rate, $GUR$ can be expressed as:
    """
    )

    st.latex(
        r"""
        q_{Glc} = \frac{\mu}{Y_{X/Glc}} + m_{Glc}
    """
    )

    st.markdown(
        """
        The glutamine uptake rate, $GlnUR$ can be expressed as:
    """
    )

    st.latex(
        r"""
        q_{Gln} = \frac{q_{max, Gln} Gln}{K_{q, Gln} + 1}
    """
    )

    st.markdown(
        """
        The lactate production rate $LPR$ is defined as:
    """
    )

    st.latex(
        r"""
        \begin{dcases}
        q_{Lac} = Y_{Lac/Glc} * q_{Glc} &\text{if } Gln > 0.5 \\
        q_{Lac} = 0 &\text{if } Gln \leq 0.5
        \end{dcases}
    """
    )

    st.markdown(
        """
        The ammonium production rate $APR$ is defined as:
    """
    )

    st.latex(
        r"""
        \begin{dcases}
        q_{Amm} = Y_{Amm/Gln} * q_{Gln} &\text{if } Gln > 0.5 \\
        q_{Amm} = 1 * 10^{-8} &\text{if } Gln \leq 0.5
        \end{dcases}
    """
    )

    st.markdown(
        """
        The Protein Production Rate $PRR$ is defined as:
    """
    )

    st.latex(
        r"""
        q_P = (\alpha\mu + \beta)\frac{K_{l3, Amm}}{K_{l3, Amm} + Amm}
    """
    )
