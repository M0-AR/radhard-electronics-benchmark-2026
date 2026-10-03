"""Make 10s demo: Weibull sweep + TID sweep -> GIF + MP4 (ffmpeg-free fallback).
Uses matplotlib animation (Pillow for GIF). MP4 via imageio-ffmpeg if present else GIF only.
Step-by-step: LET sweep draws Weibull curves; dose sweep draws TID; ends on RHA table.
"""
import os, math, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from radhard.effects import weibull_cross_section, tid_vth_shift_mv, REFERENCE_PARTS

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
lets = [0.3+i*0.8 for i in range(80)]
doses = [i*4 for i in range(76)]

def update(f):
    ax1.clear(); ax2.clear()
    n = max(2, f+1)
    xs = lets[:n]
    for pname, col in zip(["SRAM_65nm_bulk_SEU", "SRAM_RHBD_SEU"], ["#e74c3c", "#2ecc71"]):
        p = REFERENCE_PARTS[pname]
        ys = [weibull_cross_section(L, p["let_th"], p["sigma_sat"], p["W"], p["s"]) for L in xs]
        ax1.plot(xs, ys, color=col, label=pname.split("_")[1])
    ax1.set_xscale("log"); ax1.set_yscale("log"); ax1.set_ylim(1e-12, 2e-7)
    ax1.set_xlabel("LET [MeV-cm2/mg]"); ax1.set_ylabel("sigma [cm2]")
    ax1.set_title(f"SEE Weibull sweep  f={f}"); ax1.legend(fontsize=7); ax1.grid(alpha=0.3, which="both")
    dd = doses[:n]
    for t, col in zip(["planar_180nm", "finfet_7nm"], ["#e67e22", "#3498db"]):
        ys = [tid_vth_shift_mv(d, t) for d in dd]
        ax2.plot(dd, ys, color=col, label=t)
    ax2.set_xlabel("TID [krad(Si)]"); ax2.set_ylabel("Vth shift [mV]")
    ax2.set_title("TID: planar degrades, FinFET flat"); ax2.legend(fontsize=7); ax2.grid(alpha=0.3)
    fig.suptitle("radhard benchmark — live demo (EXP02+EXP03)", fontsize=11)
    fig.tight_layout()

ani = FuncAnimation(fig, update, frames=60, interval=150)
gif = os.path.join(OUT, "demo.gif")
ani.save(gif, writer="pillow", dpi=100)
print("saved", gif, os.path.getsize(gif), "bytes")
# MP4 if ffmpeg available
try:
    mp4 = os.path.join(OUT, "demo.mp4")
    ani.save(mp4, writer="ffmpeg", fps=8, dpi=100)
    print("saved", mp4, os.path.getsize(mp4), "bytes")
except Exception as e:
    print("mp4 skipped (ffmpeg missing):", e)
