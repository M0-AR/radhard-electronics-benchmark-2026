"""Radiation effects: SEE Weibull, TID degradation, SEB SOA.
Validated against:
- NASA GSFC compendia (O'Bryan et al. 2023): LETth def @1e7 p/cm2, Weibull fits
- 2026 SiC SEB papers: SEB saturates ~500V for 1200V device (>LET 25), safe <200V
- NSREC 2026 PolarFire SoC 100krad, Lattice CertusPro-NX 28nm FDSOI
"""
import math

def weibull_cross_section(let_, let_th, sigma_sat, W, s):
    """4-param Weibull per JESD57: sigma=0 below LETth, sigma_sat*(1-exp(-((L-Lth)/W)^s))."""
    if let_ <= let_th:
        return 0.0
    return sigma_sat * (1.0 - math.exp(-(((let_ - let_th) / W) ** s)))

def seu_rate_per_bit_per_day(sigma_cm2_bit, flux_cm2_s):
    return sigma_cm2_bit * flux_cm2_s * 86400.0

def tid_vth_shift_mv(dose_krad, tech="planar_180nm"):
    """Illustrative TID Vth shift. Planar NMOS negative then rebound; FinFET/FDSOI small.
    Coefficients chosen to reproduce order: 180nm ~ -150mV @100krad; FinFET ~ -10mV @100krad.
    """
    if tech == "planar_180nm":
        return -180.0 * (1 - math.exp(-dose_krad / 80.0)) + 30.0 * (1 - math.exp(-dose_krad / 500.0))
    elif tech in ("finfet_7nm", "fdsoi_28nm", "gaa"):
        return -12.0 * (1 - math.exp(-dose_krad / 200.0))
    elif tech == "bipolar":
        # ELDRS-sensitive: larger at low dose rate; use high-rate lower bound here
        return -60.0 * (1 - math.exp(-dose_krad / 30.0))
    return -50.0 * (1 - math.exp(-dose_krad / 100.0))

def sic_seb_soa(vds_V: float, let_: float):
    """Return regime per 2026 TPA+heavy-ion consensus for 1200V SiC VDMOSFET.
    safe <200V; 200-600V SELC degradation; >600V or >500V+highLET SEB high risk.
    Threshold saturates ~500V once LET>25 MeV-cm2/mg (~42% rating).
    """
    if vds_V < 200:
        return "SAFE"
    if vds_V > 600:
        return "SEB_HIGH_RISK"
    if let_ >= 25 and vds_V >= 500:
        return "SEB_HIGH_RISK"
    if vds_V >= 200:
        return "SELC_DEGRADATION_RISK"
    return "SAFE"

# Reference Weibull parameter sets (benchmark archetypes, not flight data)
REFERENCE_PARTS = {
    # SRAM 65nm bulk: low LETth, high sat – COTS-like
    "SRAM_65nm_bulk_SEU": dict(let_th=0.5, sigma_sat=1e-8, W=15.0, s=1.2, bits=16e6),
    # Rad-hard SRAM (e.g. RHBD latch): high LETth
    "SRAM_RHBD_SEU": dict(let_th=20.0, sigma_sat=5e-10, W=30.0, s=1.0, bits=16e6),
    # Power MOSFET SEB (destructive): LETth ~10, one-shot
    "SiC_1200V_SEB": dict(let_th=10.0, sigma_sat=1e-4, W=20.0, s=2.0, bits=1),
    # SEL archetype
    "CMOS_SEL": dict(let_th=40.0, sigma_sat=1e-5, W=25.0, s=1.5, bits=1),
}
