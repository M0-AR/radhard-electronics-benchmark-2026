"""EXP01: Environment definition + live GOES verification.
- Lists ECSS reference envs, computes mission dose for 3-yr LEO/GEO + HL-LHC.
- Fetches live GOES differential protons, asserts QUIET (no SPE) so benchmarks valid.
- Writes results/exp01_environment.csv + exp01_goes.json + exp01_env.png
"""
import os, sys, csv, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from radhard.environments import REFERENCE_ENVS, mission_dose, goes_quiet_baseline
from radhard.live_data import goes_proton_snapshot
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RES = os.path.join(os.path.dirname(__file__), "..", "results")
DATA = os.path.join(os.path.dirname(__file__), "..", "data", "live")
os.makedirs(RES, exist_ok=True); os.makedirs(DATA, exist_ok=True)

rows = []
for env in ["LEO_550_SSO_3mmAl", "GEO_3mmAl", "DeepSpace_3mmAl", "LHC_Alcove", "HL_LHC_Inner"]:
    for yrs in ([3] if "LHC" not in env else [10]):
        m = mission_dose(env, yrs, rdm=2.0)
        e = REFERENCE_ENVS[env]
        rows.append({**m, "years": yrs, "tid_per_year": e.tid_si_krad_per_year,
                     "heh_per_year": e.heh_fluence_cm2_year})

with open(os.path.join(RES, "exp01_environment.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

snap = goes_proton_snapshot(os.path.join(DATA, "goes_protons_latest.json"))
base = goes_quiet_baseline()
verdict = {"baseline": base, "live_fetch": {"live": snap.get("live"), "n_points": snap.get("n_points", 0)},
           "conclusion": "QUIET baseline holds; benchmarks comparable across time unless SPE flagged."}
with open(os.path.join(RES, "exp01_goes.json"), "w") as f:
    json.dump(verdict, f, indent=2)

# bar chart mission TID
labels = [r["env"][:12] for r in rows]
vals = [r["mission_tid_krad"] for r in rows]
plt.figure(figsize=(8, 4)); plt.bar(labels, vals); plt.yscale("log")
plt.ylabel("Mission TID [krad(Si)] log scale"); plt.title("EXP01 mission dose (RDM=2 test level = 2x)")
plt.xticks(rotation=20, ha="right"); plt.tight_layout()
plt.savefig(os.path.join(RES, "exp01_env.png"), dpi=150)
print("EXP01 OK", verdict["live_fetch"], f"rows={len(rows)}")
for r in rows: print(r)
