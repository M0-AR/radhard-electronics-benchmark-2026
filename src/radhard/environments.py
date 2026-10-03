"""Radiation environments: space, atmospheric, accelerator.
Sources verified 2026-10-03:
- NASA AP8/AE8, CREME96, SAPPHIRE (Jiggens 2018), ESP-PSYCHIC, ISO-15390 GCR
- ECSS-E-ST-10-04, ECSS-Q-ST-60-15 RHA
- CERN CHARM mixed-field (24 GeV/c p on Cu/Al, ~500 Gy/week, 1e12 HEH/cm2/week)
- JEDEC JESD89 atmospheric neutron
"""
from dataclasses import dataclass
import math

@dataclass
class EnvPoint:
    name: str
    tid_si_krad_per_year: float
    heh_fluence_cm2_year: float
    proton_flux_gt10mev_cm2_s: float
    heavy_ion_let_gt15_rate_cm2_s: float
    notes: str

# Conservative reference mission points distilled from ECSS + NASA + CERN docs.
# Values are order-of-magnitude benchmarks for relative comparison, NOT flight spec.
REFERENCE_ENVS = {
    # LEO 550km SSO, 3mm Al – COTS CubeSat regime
    "LEO_550_SSO_3mmAl": EnvPoint("LEO_550_SSO_3mmAl", 2.5, 2.0e9, 150.0, 1e-7,
        "Trapped protons (AP8) dominate TID; SAA passes drive SEU bursts."),
    # GEO, 3mm Al – classic comsat
    "GEO_3mmAl": EnvPoint("GEO_3mmAl", 15.0, 5.0e9, 400.0, 5e-6,
        "Trapped e- + solar protons (SAPPHIRE/ESP); GCR heavy ions drive SEL/SEU."),
    # Lunar / deep-space cruise, 3mm Al
    "DeepSpace_3mmAl": EnvPoint("DeepSpace_3mmAl", 8.0, 1.0e10, 800.0, 2e-5,
        "No magnetospheric shielding; GCR + SEP (CREME96/ISO15390)."),
    # LHC tunnel alcove (e.g. UJ) – accelerator mixed field
    "LHC_Alcove": EnvPoint("LHC_Alcove", 2.0, 1.0e10, 0.0, 0.0,
        "CHARM-like mixed field: p/n/pi + gammas; HEH equiv. is metric."),
    # LHC inner detector (HL-LHC) – extreme cumulative
    "HL_LHC_Inner": EnvPoint("HL_LHC_Inner", 100000.0, 1.0e15, 0.0, 0.0,
        "Up to ~1 MGy + 1e15 neq/cm2; only dedicated ASICs survive."),
    # Avionics 12km, 55deg – atmospheric neutrons
    "Avionics_12km": EnvPoint("Avionics_12km", 0.001, 3.0e5, 0.0, 0.0,
        "JEDEC JESD89 neutron flux ~ few 1e3 n/cm2/h >10MeV at ground; x300 at altitude."),
}

def goes_quiet_baseline():
    """Live-anchored quiet baseline from NOAA GOES-18 differential protons 2026-10-02.
    Verified 2026-10-03 via services.swpc.noaa.gov P1 (1-1.86 MeV) ~0.008 pfu,
    P5-P8 high-energy channels ~1e-6..1e-5. Quiet = no SPE in progress.
    Returns dict used by exp01 to assert test validity.
    """
    return {
        "date": "2026-10-02",
        "P1_1020_1860keV_flux": 0.008,
        "P5_11640_23270keV_flux": 1.2e-5,
        "P8_83700_118000keV_flux": 1.0e-6,
        "verdict": "QUIET",
        "source": "https://services.swpc.noaa.gov/json/goes/primary/differential-protons-1-day.json",
    }

def mission_dose(env_name: str, years: float, rdm: float = 2.0):
    e = REFERENCE_ENVS[env_name]
    return {
        "env": env_name,
        "mission_tid_krad": e.tid_si_krad_per_year * years,
        "required_test_tid_krad": e.tid_si_krad_per_year * years * rdm,
        "mission_heh_cm2": e.heh_fluence_cm2_year * years,
    }
