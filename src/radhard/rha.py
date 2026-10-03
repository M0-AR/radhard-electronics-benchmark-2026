"""RHA: margins, confidence, rate prediction, alpha-factor.
ECSS-Q-ST-60-15: RDM>=2 for TID/TNID; LETth SEL>75 (no SEL), SEB/SEGR>37 normal incidence.
Coronetti et al. system-level: alpha-factor rescales hadron test counts to orbit rates.
"""
import math

def rdm(failure_level: float, mission_level: float) -> float:
    return failure_level / mission_level if mission_level > 0 else float("inf")

def rha_pass_tid(mission_krad: float, test_failure_krad: float, required_rdm: float = 2.0):
    margin = rdm(test_failure_krad, mission_krad)
    return {"RDM": margin, "PASS": margin >= required_rdm, "required_RDM": required_rdm}

def rha_pass_sel(let_th_sel: float) -> dict:
    return {"LETth_SEL": let_th_sel, "PASS": let_th_sel > 75.0, "criterion": "LETth>75 MeV-cm2/mg"}

def rha_pass_seb(let_th_seb: float) -> dict:
    return {"LETth_SEB": let_th_seb, "PASS": let_th_seb > 37.0, "criterion": "LETth>37 normal incidence + derating"}

def alpha_factor_orbit_rate(n_events_test: int, test_fluence_cm2: float,
                            alpha: float, mission_fluence_cm2: float) -> float:
    """Expected on-orbit count = N_test * alpha * (mission_fluence/test_fluence).
    Alpha ~ orbit-dependent, weakly beam-dependent (Coronetti). Typical 0.5-5.
    """
    if test_fluence_cm2 <= 0:
        return 0.0
    return n_events_test * alpha * (mission_fluence_cm2 / test_fluence_cm2)

def weibull_rate_integral(sigma_sat, let_th, W, s, lets, fluxes):
    """Sum sigma(L)*phi(L)*dL approx discrete. lets/fluxes same length (flux per LET bin)."""
    total = 0.0
    from .effects import weibull_cross_section
    for L, phi in zip(lets, fluxes):
        total += weibull_cross_section(L, let_th, sigma_sat, W, s) * phi
    return total  # events/s (per device if sigma per device)
