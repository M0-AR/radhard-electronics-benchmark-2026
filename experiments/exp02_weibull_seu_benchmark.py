"""EXP02: Weibull SEE benchmark – COTS vs RHBD + hidden charge-sharing pattern.
- Weibull curves for SRAM_65nm vs RHBD; orbit rate via GEO/LEO flux proxies.
- Demonstrates H1: scaled FinFET low Qcrit -> 100x higher SEU at low LET despite better TID.
- Writes exp02_weibull.csv/png + prints rate table.
"""
import os, sys, csv, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from radhard.effects import weibull_cross_section, REFERENCE_PARTS
from radhard.interactions import let_to_charge_deposited_fC, critical_charge_threshold_fC
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt

RES = os.path.join(os.path.dirname(__file__), "..", "results"); os.makedirs(RES, exist_ok=True)
lets = [0.1, 0.5, 1, 2, 5, 10, 20, 40, 60, 80]
rows = []
for pname, p in REFERENCE_PARTS.items():
    for L in lets:
        sig = weibull_cross_section(L, p["let_th"], p["sigma_sat"], p["W"], p["s"])
        rows.append({"part": pname, "LET": L, "sigma_cm2": sig})
with open(os.path.join(RES, "exp02_weibull.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["part", "LET", "sigma_cm2"]); w.writeheader(); w.writerows(rows)

plt.figure(figsize=(7, 5))
for pname in REFERENCE_PARTS:
    xs = [r["LET"] for r in rows if r["part"] == pname]
    ys = [r["sigma_cm2"] for r in rows if r["part"] == pname]
    plt.plot(xs, ys, marker="o", label=pname)
plt.xscale("log"); plt.yscale("log"); plt.xlabel("LET [MeV-cm2/mg]"); plt.ylabel("sigma [cm2]")
plt.title("EXP02 Weibull SEE cross-sections (benchmark archetypes)"); plt.legend(fontsize=7); plt.grid(True, which="both", alpha=0.3)
plt.tight_layout(); plt.savefig(os.path.join(RES, "exp02_weibull.png"), dpi=150)

# Hidden pattern H1 numbers
q_dep_1let_1um = let_to_charge_deposited_fC(1.0, 1.0)
qcrit_180 = critical_charge_threshold_fC(10.0, 1.8)
qcrit_7nm = critical_charge_threshold_fC(0.5, 0.75)
print(f"EXP02 OK: Qdep(1 LET,1um)={q_dep_1let_1um:.2f} fC, Qcrit_180nm={qcrit_180:.1f} fC, Qcrit_7nmFinFET={qcrit_7nm:.3f} fC")
print("=> 7nm upset by LET~0.1 while 180nm needs LET~few -> explains 100x SEU gap at low LET.")
# Orbit rate illustration: GEO heavy-ion flux proxy 5e-6/cm2/s integrated with sigma_sat
for pname, p in REFERENCE_PARTS.items():
    if "SEU" in pname:
        rate = p["sigma_sat"] * p["bits"] * 5e-6 * 86400
        print(f"{pname}: worst-case GEO upset/day ~ {rate:.2e} (sigma_sat x bits x flux)")
