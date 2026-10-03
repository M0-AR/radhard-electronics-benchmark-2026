"""EXP03: TID degradation + SiC SEB safe-operating-area.
- Vth shift vs dose for planar vs FinFET/FDSOI vs bipolar (ELDRS bound).
- SiC 1200V SOA map per 2026 consensus: safe <200V, SELC 200-600V, SEB high risk >600V or >=500V & LET>=25.
- Writes exp03_tid.csv/png + exp03_soa.csv
"""
import os, sys, csv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from radhard.effects import tid_vth_shift_mv, sic_seb_soa
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt

RES = os.path.join(os.path.dirname(__file__), "..", "results"); os.makedirs(RES, exist_ok=True)
doses = [0, 5, 10, 20, 50, 100, 200, 300]
techs = ["planar_180nm", "finfet_7nm", "fdsoi_28nm", "bipolar"]
rows = [{"tech": t, "dose_krad": d, "dvth_mV": tid_vth_shift_mv(d, t)} for t in techs for d in doses]
with open(os.path.join(RES, "exp03_tid.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["tech", "dose_krad", "dvth_mV"]); w.writeheader(); w.writerows(rows)
plt.figure(figsize=(7, 4.5))
for t in techs:
    xs = [r["dose_krad"] for r in rows if r["tech"] == t]
    ys = [r["dvth_mV"] for r in rows if r["tech"] == t]
    plt.plot(xs, ys, marker="o", label=t)
plt.xlabel("TID [krad(Si)]"); plt.ylabel("Vth shift [mV]"); plt.title("EXP03 TID Vth shift: planar degrades, FinFET/FDSOI flat")
plt.legend(fontsize=8); plt.grid(alpha=0.3); plt.tight_layout()
plt.savefig(os.path.join(RES, "exp03_tid.png"), dpi=150)

vds_list = [100, 200, 300, 400, 500, 650, 800]
let_list = [5, 15, 25, 40, 75]
soa = [{"Vds": v, "LET": L, "regime": sic_seb_soa(v, L)} for v in vds_list for L in let_list]
with open(os.path.join(RES, "exp03_soa.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["Vds", "LET", "regime"]); w.writeheader(); w.writerows(soa)
print("EXP03 OK: planar@100krad=%.1f mV, finfet@100krad=%.1f mV" % (
    tid_vth_shift_mv(100, "planar_180nm"), tid_vth_shift_mv(100, "finfet_7nm")))
print("SOA check 500V@30LET =", sic_seb_soa(500, 30), "| 150V@75LET =", sic_seb_soa(150, 75))
