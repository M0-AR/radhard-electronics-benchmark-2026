"""Mitigation: TMR, ECC/scrubbing, redundancy.
Sources: Siegle et al. Virtex-4 TMR+scrub; Liu 2024 FPGA review; RADNEXT WP6 system-level.
"""
import math

def tmr_reliability(r_single: float) -> float:
    """3-module majority voter (perfect voter): R_tmr = 3R^2 - 2R^3."""
    return 3 * r_single**2 - 2 * r_single**3

def tmr_with_voter(r_single: float, r_voter: float) -> float:
    return (3 * r_single**2 - 2 * r_single**3) * r_voter

def scrubbed_mtbu_hours(upset_rate_per_bit_per_hour: float, bits: float,
                        scrub_interval_s: float, ecc_correctable_bits: int = 1) -> float:
    """Mean time to uncorrectable (2+ errors in same word between scrubs).
    Word = 39 bits (32+7 SECDED). Approx Poisson per word per scrub interval.
    MTBU = scrub_interval / P_uncorrectable_per_interval_system.
    Non-linear flux dependence revealed by Zebrev 2014: doubling flux more than doubles failure when scrub limited.
    """
    words = bits / 32.0
    lam_word = upset_rate_per_bit_per_hour * 39.0 * (scrub_interval_s / 3600.0)
    # P(>=2) = 1 - e^-l (1+l)
    p_uncorr_word = 1 - math.exp(-lam_word) * (1 + lam_word)
    p_sys = 1 - (1 - p_uncorr_word) ** words if words < 1e9 else words * p_uncorr_word
    if p_sys <= 0:
        return float("inf")
    return (scrub_interval_s / 3600.0) / p_sys

def ecc_overhead_pct(data_bits: int = 32, check_bits: int = 7) -> float:
    return 100.0 * check_bits / data_bits

def availability_with_reboot(mttf_h: float, mttr_h: float) -> float:
    return mttf_h / (mttf_h + mttr_h)
