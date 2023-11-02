def mu_func(res, param):
    """
    Cell growth function
    """

    mu = (
        (param["mu_max"] * res["Glc"] / (param["Ks_Glc"] + res["Glc"]))
        * ((0.5 * param["Ks_Gln"] + res["Gln"]) / (param["Ks_Gln"] + res["Gln"]))
        * (param["Kl1_Amm"] / (param["Kl1_Amm"] + res["Amm"]))
        * (param["Kl1_Lac"] / (param["Kl1_Lac"] + res["Lac"]))
    )

    return mu


def k_D(res, param):
    """
    Cell death function
    """
    kD = 0.1
    if res["Glc"] > 0:
        kD = 0.05 * (1 - param["Kl2_Amm"] / (param["Kl2_Amm"] + res["Amm"])) + 0.05 * (
            1 - param["Kl2_Lac"] / (param["Kl2_Lac"] + res["Lac"])
        )
    return kD


def GUR(res, param):
    """
    Glucose uptake rate (GUR)
    """
    q_Glc = 0
    if res["Glc"] > 0:
        q_Glc = (res["mu"] / param["Yx_Glc"]) + param["m_Glc"]
    return q_Glc


def GlnUR(res, param):
    """
    Glutamine uptake rate (GlnUR)
    """
    q_Gln = 0
    if res["Gln"] > 0:
        q_Gln = (param["qmax_Gln"] * res["Gln"]) / (param["Kq_Gln"] + res["Gln"])
    return q_Gln


def LPR(res, param):
    """
    Lactate production rate
    """
    q_Lac = 0
    if res["Gln"] > 0.5:
        q_Lac = param["Ylac_Glc"] * res["q_Glc"]
    return q_Lac


def APR(res, param):
    """
    Ammonium production rate
    """
    q_Amm = 1e-8
    if res["Gln"] > 0.5:
        q_Amm = param["Yamm_Gln"] * res["q_Gln"]
    return q_Amm


def PPR(res, param):
    """
    Product production rate
    """
    q_P = (
        (param["alpha"] * res["mu"] + param["beta"])
        * param["Kl3_Amm"]
        / (param["Kl3_Amm"] + res["Amm"])
    )
    return q_P


param = {
    "mu_max": 0.045,  # 1/h,
    "Ks_Glc": 2.5,  # mM,
    "Ks_Gln": 0.5,
    "Yx_Glc": 8e5,  # c/mmol,
    "m_Glc": 4.5e-7,  # mmol/c*h,
    "qmax_Gln": 2.5e-7,  # mM*mL/c*h,
    "Kq_Gln": 10,  # mM,
    "Ylac_Glc": 0.20,  # M/M,
    "Yamm_Gln": 1.50,
    "alpha": 0,  # ug/c,
    "beta": 6e-6,  # ug/c*h,
    "Kl1_Lac": 300,  # mM,
    "Kl2_Lac": 30,
    "Kl1_Amm": 20,
    "Kl2_Amm": 25,
    "Kl3_Amm": 5,
}


def init_sim(
    X_0=2.0e5,  # Cells/mL
    Glc_0=35.0,  # mM
    Gln_0=4.0,
    Lac_0=0.0,
    Amm_0=0.0,
    P_0=0.0,  # mg/mL
    V_0=1000.0,  # L
):
    # initialization
    res = {}
    res["X"] = X_0
    res["Glc"] = Glc_0
    res["Gln"] = Gln_0
    res["Lac"] = Lac_0
    res["Amm"] = Amm_0
    res["P"] = P_0
    res["V"] = V_0
    res["t"] = 0.0

    res["F_Glc"] = 0
    res["F_Gln"] = 0
    res["F_B"] = 0

    res["mu"] = mu_func(res, param)
    res["kD"] = k_D(res, param)
    res["q_Glc"] = GUR(res, param)
    res["q_Gln"] = GlnUR(res, param)
    res["q_Lac"] = LPR(res, param)
    res["q_Amm"] = APR(res, param)
    res["q_P"] = PPR(res, param)

    return res


def gen(data, Glc_F, Gln_F, F_Glc, F_Gln, F_B, t_max=250, dt=0.5):
    res = data.to_dict()
    n_points = int(t_max / dt) + 1

    for _ in range(n_points):
        if res["t"] >= t_max:
            break

        t = res["t"] + dt

        # Mass Balance equations
        X = res["X"] * (
            1 + dt * (res["mu"] - res["kD"] - (F_Glc + F_Gln + F_B) / res["V"])
        )

        Glc = res["Glc"] + dt * (
            F_Glc * (Glc_F - res["Glc"]) / res["V"]
            - (F_Gln + F_B) * res["Glc"] / res["V"]
            - res["X"] * res["q_Glc"]
        )
        if Glc < 0:
            Glc = 0

        Gln = res["Gln"] + dt * (
            F_Gln * (Gln_F - res["Gln"]) / res["V"]
            - (F_Glc + F_B) * res["Gln"] / res["V"]
            - res["X"] * res["q_Gln"]
        )
        if Gln < 0:
            Gln = 0

        Lac = res["Lac"] + dt * (
            res["q_Lac"] * res["X"] - (F_Glc + F_Gln + F_B) * res["Lac"] / res["V"]
        )
        Amm = res["Amm"] + dt * (
            res["q_Amm"] * res["X"] - (F_Glc + F_Gln + F_B) * res["Amm"] / res["V"]
        )
        P = res["P"] + dt * (
            res["q_P"] * res["X"] - (F_Glc + F_Gln + F_B) * res["P"] / res["V"]
        )
        V = res["V"] + dt * (F_Glc + F_Gln + F_B)

        # store results for next calc
        res["t"] = t
        res["X"] = X
        res["Glc"] = Glc
        res["Gln"] = Gln
        res["Lac"] = Lac
        res["Amm"] = Amm
        res["P"] = P
        res["V"] = V

        res["F_Glc"] = F_Glc
        res["F_Gln"] = F_Gln
        res["F_B"] = F_B

        # kinetics
        res["mu"] = mu_func(res, param)
        res["kD"] = k_D(res, param)
        res["q_Glc"] = GUR(res, param)
        res["q_Gln"] = GlnUR(res, param)
        res["q_Lac"] = LPR(res, param)
        res["q_Amm"] = APR(res, param)
        res["q_P"] = PPR(res, param)

        yield res
