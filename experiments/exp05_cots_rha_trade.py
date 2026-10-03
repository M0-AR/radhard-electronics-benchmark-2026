"""EXP05: COTS vs rad-hard trade + RHA pass/fail + alpha-factor orbit projection.
- Mission: 3-yr GEO (45 krad) vs 3-yr LEO (7.5 krad). Parts: COTS ADC (fails 20krad, SEL LETth 8),
  RHBD FPGA (fails 300krad, SEL LETth 80), SiC switch (SEB LETth 12 -> derate required).
- RDM>=2, SEL>75, SEB>37 criteria per ECSS/Campola.
- Alpha-factor: CHARM test N=3 events @1e11 HEH -> GEO mission 1.5e10 HEH, alpha=1.2.
- Writes exp05_rha.csv + prints verdict table (benchmark standard).
"""
import os, sys, csv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from radhard.rha import rha_pass_tid, rha_pass_sel, rha_pass_seb, alpha_factor_orbit_rate

RES = os.path.join(os.path.dirname(__file__), "..", "results"); os.makedirs(RES, exist_ok=True)
missions = {"GEO_3yr": 45.0, "LEO_3yr": 7.5}
parts = {
    "COTS_ADC": {"fail_krad": 20.0, "sel_th": 8.0, "seb_th": 999.0},
    "RHBD_FPGA": {"fail_krad": 300.0, "sel_th": 80.0, "seb_th": 999.0},
    "SiC_1200V_at_800V": {"fail_krad": 500.0, "sel_th": 999.0, "seb_th": 12.0},
    "SiC_1200V_derated_150V": {"fail_krad": 500.0, "sel_th": 999.0, "seb_th": 60.0},
}
rows = []
for m, dose in missions.items():
    for p, v in parts.items():
        tid = rha_pass_tid(dose, v["fail_krad"])
        sel = rha_pass_sel(v["sel_th"]) if v["sel_th"] < 900 else {"PASS": True, "LETth_SEL": 999}
        seb = rha_pass_seb(v["seb_th"]) if v["seb_th"] < 900 else {"PASS": True, "LETth_SEB": 999}
        overall = tid["PASS"] and sel["PASS"] and seb["PASS"]
        rows.append({"mission": m, "part": p, "mission_krad": dose,
                     "RDM": round(tid["RDM"], 2), "TID_PASS": tid["PASS"],
                     "SEL_PASS": sel["PASS"], "SEB_PASS": seb["PASS"], "RHA_PASS": overall})
with open(os.path.join(RES, "exp05_rha.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
proj = alpha_factor_orbit_rate(3, 1e11, 1.2, 1.5e10)
print("EXP05 RHA benchmark (RDM>=2, SEL>75, SEB>37):")
for r in rows: print(r)
print(f"Alpha-factor projection: 3 events @CHARM 1e11 -> GEO mission expects {proj:.2f} events (alpha=1.2)")
print("Hidden pattern: COTS core may pass SEE but LDO/regulator TID kills system first (Orin 19krad, SEE-Tester 150Gy).")
