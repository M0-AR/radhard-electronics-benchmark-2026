import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from radhard.interactions import let_to_charge_deposited_fC
from radhard.effects import weibull_cross_section, sic_seb_soa
from radhard.mitigation import tmr_reliability
from radhard.rha import rha_pass_tid, alpha_factor_orbit_rate

def test_weibull_below_threshold_zero():
    assert weibull_cross_section(5, 10, 1e-8, 20, 1.5) == 0.0

def test_weibull_monotonic():
    a = weibull_cross_section(20, 10, 1e-8, 20, 1.5)
    b = weibull_cross_section(60, 10, 1e-8, 20, 1.5)
    assert b > a > 0

def test_charge_order():
    q = let_to_charge_deposited_fC(1.0, 1.0)
    assert 5 < q < 20  # ~10.4 fC expected

def test_sic_soa():
    assert sic_seb_soa(150, 75) == "SAFE"
    assert sic_seb_soa(500, 30) == "SEB_HIGH_RISK"
    assert sic_seb_soa(300, 10) == "SELC_DEGRADATION_RISK"

def test_tmr_gain():
    assert abs(tmr_reliability(0.9) - 0.972) < 1e-6

def test_rha():
    assert rha_pass_tid(45, 300)["PASS"] is True
    assert rha_pass_tid(45, 20)["PASS"] is False
    assert alpha_factor_orbit_rate(3, 1e11, 1.2, 1.5e10) > 0
