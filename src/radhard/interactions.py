"""Particle-matter interactions: LET, TID, NIEL/DDD.
Bethe-Bloch (restricted), charge deposition, dose conversions.
"""
import math

# Si constants
RHO_SI = 2.33  # g/cm3
E_EH_SI = 3.6  # eV per e-h pair
Q_E = 1.602e-19  # C

def let_to_charge_deposited_fC(let_mev_cm2_mg: float, path_um: float) -> float:
    """Charge deposited in Si: Q[fC] = LET * rho * L * (1e-15 J/eV conv) / E_eh.
    LET in MeV-cm2/mg, path in um. 1 MeV = 1.602e-13 J.
    dE = LET * rho(mg/cm3=2330) * L(cm). N_pairs = dE_MeV*1e6/3.6.
    """
    rho_mg_cm3 = RHO_SI * 1000.0
    L_cm = path_um * 1e-4
    dE_MeV = let_mev_cm2_mg * rho_mg_cm3 * L_cm
    n_pairs = dE_MeV * 1e6 / E_EH_SI
    return n_pairs * Q_E * 1e15  # fC

def critical_charge_threshold_fC(node_capacitance_fF: float, vdd_V: float) -> float:
    """Qcrit ~ C * V. Scaled nodes: 28nm ~1-2 fC, 7nm FinFET ~0.2-0.5 fC."""
    return node_capacitance_fF * vdd_V  # fC since fF*V = fC

def rad_to_gy(rad: float) -> float:
    return rad * 0.01

def krad_to_TID_Gy(krad: float) -> float:
    return krad * 10.0

def heh_to_TID_approx_Gy(heh_cm2: float) -> float:
    """CHARM rule-of-thumb: 1e12 HEH/cm2/week <-> ~500 Gy/week at max position.
    => ~5e-10 Gy per HEH/cm2. Position-dependent; use as scaling benchmark only.
    """
    return heh_cm2 * 5e-10

def niel_hardness_factor(particle: str) -> float:
    """Illustrative NIEL hardness factors normalized to 1 MeV neutrons."""
    table = {"1MeV_neutron": 1.0, "24GeV_proton": 0.6, "64MeV_proton": 1.4,
             "14MeV_neutron": 1.7, "Co60_gamma": 0.001}
    return table.get(particle, 1.0)
