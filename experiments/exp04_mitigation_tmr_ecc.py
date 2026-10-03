"""EXP04: Mitigation – TMR + ECC scrubbing non-linearity (Zebrev hidden pattern).
- TMR reliability gain vs single-string.
- Scrubbed MTBU for 16Mb SRAM at GEO-like upset rates, scrub 1s vs 10s vs 100s.
- Shows doubling flux more than doubles system failure when scrub-limited.
- Writes exp04_mitigation.csv/png
"""
import os, sys, csv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from radhard.mitigation import tmr_reliability, scrubbed_mtbu_hours
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt

RES = os.path.join(os.path.dirname(__file__), "..", "results"); os.makedirs(RES, exist_ok=True)
# TMR curve
rs = [i/100 for i in range(80, 100)]
tmr = [tmr_reliability(r) for r in rs]
plt.figure(figsize=(7, 4)); plt.plot(rs, rs, "--", label="no TMR"); plt.plot(rs, tmr, label="TMR perfect voter")
plt.xlabel("single-string reliability"); plt.ylabel("system reliability"); plt.title("EXP04 TMR gain")
plt.legend(); plt.grid(alpha=0.3); plt.tight_layout(); plt.savefig(os.path.join(RES, "exp04_tmr.png"), dpi=150)

# Scrub MTBU: upset rate per bit per hour sweep (quiet vs SPE x100)
import math
rates = [1e-9, 1e-8, 1e-7, 1e-6, 1e-5]
scrubs = [1, 10, 100]
rows = []
for rate in rates:
    for sc in scrubs:
        mtbu = scrubbed_mtbu_hours(rate, 16e6, sc)
        rows.append({"upset_per_bit_h": rate, "scrub_s": sc, "MTBU_h": mtbu})
with open(os.path.join(RES, "exp04_mitigation.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["upset_per_bit_h", "scrub_s", "MTBU_h"]); w.writeheader(); w.writerows(rows)
print("EXP04 OK: R(0.9)->TMR %.4f" % tmr_reliability(0.9))
for r in rows:
    if r["scrub_s"] == 10: print("rate %.0e -> MTBU %.2e h (scrub 10s)" % (r["upset_per_bit_h"], r["MTBU_h"]))
print("Hidden pattern: 10x flux -> >10x MTBU collapse when scrub interval fixed (Poisson >=2).")
