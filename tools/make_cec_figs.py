# -*- coding: utf-8 -*-
"""Column-width figures for the IEEE CEC version (single column = 3.45 in).

The full-paper figures are designed for a 7.2 in text width; squeezed into a
3.45 in column their labels are unreadable, so the CEC variants are regenerated
at column width with only the two profiles that matter (P2 baseline, P4 extreme).
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "tools", "baseline_data.json")
SIM = os.path.join(ROOT, "tools", "sim_data.json")
OUT = os.path.join(ROOT, "paper", "cec", "assets")
COL = 3.42  # inches, IEEE single column text width

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 6.4,
    "axes.labelsize": 6.6,
    "axes.titlesize": 7.0,
    "xtick.labelsize": 6.0,
    "ytick.labelsize": 6.0,
    "legend.fontsize": 5.9,
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,
    "xtick.major.size": 2.0,
    "ytick.major.size": 2.0,
})

METHODS = ["RS", "SP-EA", "SA", "COA-T", "LRLS"]
LABEL = {"RS": "RS", "SP-EA": "SP-EA", "SA": "SA", "COA-T": "COA-T",
         "LRLS": "LRLS"}
COLOR = {"RS": "#0072B2", "SP-EA": "#009E73", "SA": "#E69F00",
         "COA-T": "#CC79A7", "LRLS": "#D55E00"}
HATCH = {"P2-baseline": "", "P4-extreme": "///"}


def load():
    d = json.load(open(DATA, encoding="utf-8"))
    return {p["name"]: p for p in d["summary"]}


def fig_baselines(prof):
    """Two panels, grouped bars: 5 methods x 2 profiles."""
    fig, axes = plt.subplots(1, 2, figsize=(COL, 1.95))
    profiles = ["P2-baseline", "P4-extreme"]
    tag = {"P2-baseline": "P2", "P4-extreme": "P4"}
    x = np.arange(len(METHODS))
    w = 0.36

    for ax, key, ylab in [(axes[0], "n99", "eval. to 99% (log)"),
                          (axes[1], "vioAt99", "violations to 99%")]:
        for j, pname in enumerate(profiles):
            vals, errs = [], []
            for m in METHODS:
                v = prof[pname]["methods"][m][key]
                vals.append(np.nan if v["mean"] is None else v["mean"])
                errs.append(0 if v["sd"] is None else v["sd"])
            vals = np.array(vals, dtype=float)
            errs = np.array(errs, dtype=float)
            pos = x + (j - 0.5) * w
            hatch = HATCH[pname]
            bars = ax.bar(pos, np.nan_to_num(vals), w * 0.94,
                          yerr=np.vstack([np.minimum(errs, np.nan_to_num(vals)), errs]),
                          capsize=1.4, linewidth=0.35, edgecolor="black",
                          error_kw={"elinewidth": 0.5, "capthick": 0.5})
            for b, m in zip(bars, METHODS):
                b.set_facecolor(COLOR[m])
                b.set_hatch(hatch)
                if pname == "P4-extreme":
                    b.set_alpha(0.55)
        ax.set_xticks(x)
        ax.set_xticklabels([LABEL[m] for m in METHODS], rotation=35, ha="right")
        ax.set_ylabel(ylab)
        ax.set_yscale("log" if key == "n99" else "linear")
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.grid(axis="y", linewidth=0.3, alpha=0.4)
        ax.set_axisbelow(True)

    axes[0].set_title("(a) sample efficiency", loc="left", pad=2)
    axes[1].set_title("(b) violations before threshold", loc="left", pad=2)

    from matplotlib.patches import Patch
    handles = [Patch(facecolor="0.6", edgecolor="black", linewidth=0.35, label="P2"),
               Patch(facecolor="0.6", edgecolor="black", linewidth=0.35, hatch="///",
                     label="P4")]
    fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False,
               handlelength=1.4, columnspacing=1.0, bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout(pad=0.35, rect=(0, 0.09, 1, 1))
    out = os.path.join(OUT, "fig-baselines-cec.png")
    fig.savefig(out, dpi=400, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    return out


def fig_scheduler(sim):
    """Refiner capacity N_B over the run, one step line per profile.

    A stacked area hides the point: P2 also drops to one refiner much of the
    time. Drawing N_B alone makes the P4 pinning at 1 unmistakable.
    """
    prof = {p["name"]: p for p in sim["profiles"]}
    order = ["P1-easy", "P2-default", "P3-highrisk", "P4-extreme"]
    tag = {"P1-easy": "P1 mild", "P2-default": "P2 baseline",
           "P3-highrisk": "P3 high-risk", "P4-extreme": "P4 extreme"}
    color = {"P1-easy": "#0072B2", "P2-default": "#009E73",
             "P3-highrisk": "#E69F00", "P4-extreme": "#D55E00"}
    style = {"P1-easy": (0, (1, 1)), "P2-default": (0, (4, 1.5)),
             "P3-highrisk": (0, (6, 1.5, 1, 1.5)), "P4-extreme": "solid"}

    fig, ax = plt.subplots(figsize=(COL, 1.72))
    for name in order:
        s = prof[name]["series"]
        t = [r["t"] for r in s]
        nb = [r["NB"] for r in s]
        ax.step(t, nb, where="post", color=color[name], linewidth=1.15,
                linestyle=style[name], label=tag[name])
    ax.set_xlim(0, 1100)
    ax.set_ylim(0, 4.6)
    ax.set_yticks([1, 2, 3, 4])
    ax.set_xlabel("tick", labelpad=1)
    ax.set_ylabel(r"refiners $N_B$", labelpad=1)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.grid(axis="y", linewidth=0.3, alpha=0.35)
    ax.set_axisbelow(True)
    ax.tick_params(pad=1.5)
    ax.legend(loc="upper right", ncol=1, frameon=False, handlelength=1.9,
              handletextpad=0.5, borderaxespad=0.25, labelspacing=0.28)
    fig.tight_layout(pad=0.3)
    out = os.path.join(OUT, "fig-scheduler-cec.png")
    fig.savefig(out, dpi=400, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    prof = load()
    a = fig_baselines(prof)
    b = fig_scheduler(json.load(open(SIM, encoding="utf-8")))
    for f in (a, b):
        print("wrote", f, os.path.getsize(f), "bytes")


if __name__ == "__main__":
    main()
