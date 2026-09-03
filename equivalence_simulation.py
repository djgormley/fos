"""Reproduce the numerical figure for the accompanying manuscript.

The script verifies the finite-record identity directly, estimates the
detection probability of the common statistic, and plots the loss caused by
using the nearest DFT bin for an off-grid tone.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ncx2


SEED = 20260902
N = 64
P_FA = 1e-2
TRIALS = 80_000


def main() -> None:
    rng = np.random.default_rng(SEED)
    alpha = 11 / N
    n = np.arange(N)
    s = np.exp(1j * 2 * np.pi * alpha * n)
    sigma2 = 1.0
    threshold = -np.log(P_FA)

    # Direct finite-record verification on independently generated records.
    check_trials = 4_000
    a_check = 10 ** (-14 / 20)
    w = np.sqrt(sigma2 / 2) * (
        rng.standard_normal((check_trials, N))
        + 1j * rng.standard_normal((check_trials, N))
    )
    x = a_check * s[None, :] + w
    cyclic_mean = (x @ np.conj(s)) / N
    t_cyclic = N * np.abs(cyclic_mean) ** 2 / sigma2
    t_matched = np.abs(x @ np.conj(s)) ** 2 / (sigma2 * np.vdot(s, s).real)
    max_identity_error = np.max(np.abs(t_cyclic - t_matched))
    if max_identity_error > 5e-12:
        raise RuntimeError(f"Identity check failed: {max_identity_error:g}")

    # Monte Carlo detection probabilities can be generated directly at the
    # normalized matched-filter output because that output is sufficient.
    snr_db = np.arange(-25, -4, 2)
    snr = 10 ** (snr_db / 10)
    pd_mc = []
    for rho in snr:
        z = (
            rng.standard_normal(TRIALS) + 1j * rng.standard_normal(TRIALS)
        ) / np.sqrt(2)
        t = np.abs(np.sqrt(N * rho) + z) ** 2
        pd_mc.append(np.mean(t > threshold))
    pd_mc = np.asarray(pd_mc)
    pd_theory = ncx2.sf(2 * threshold, df=2, nc=2 * N * snr)

    # Nearest-bin response as a function of frequency offset in DFT bins.
    offset_bins = np.linspace(-1.5, 1.5, 1601)
    delta = offset_bins / N
    numerator = np.sin(np.pi * N * delta)
    denominator = N * np.sin(np.pi * delta)
    response = np.ones_like(delta)
    nonzero = np.abs(delta) > 1e-15
    response[nonzero] = np.abs(numerator[nonzero] / denominator[nonzero]) ** 2
    response_db = 10 * np.log10(np.maximum(response, 1e-6))
    half_bin_loss = 10 * np.log10(
        (np.sin(np.pi / 2) / (N * np.sin(np.pi / (2 * N)))) ** 2
    )

    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.size": 9.2,
            "axes.labelsize": 9.2,
            "axes.titlesize": 9.6,
            "legend.fontsize": 8.2,
        }
    )
    fig, axes = plt.subplots(1, 2, figsize=(7.25, 2.75), constrained_layout=True)

    ax = axes[0]
    ax.plot(snr_db, pd_theory, color="#194c80", linewidth=1.8, label="Noncentral $\\chi^2$ theory")
    ax.plot(
        snr_db,
        pd_mc,
        linestyle="none",
        marker="o",
        markersize=4.3,
        markerfacecolor="white",
        markeredgewidth=1.2,
        color="#b4462a",
        label="Cyclic = matched-filter Monte Carlo",
    )
    ax.set_xlabel("Per-sample SNR (dB)")
    ax.set_ylabel("Detection probability")
    ax.set_title(f"(a) Exact decision-statistic identity ($N={N}$)")
    ax.set_ylim(-0.02, 1.02)
    ax.set_xlim(snr_db[0], snr_db[-1])
    ax.grid(True, alpha=0.28)
    ax.legend(loc="lower right", frameon=True)
    ax.text(
        0.03,
        0.94,
        rf"$P_{{\rm FA}}={P_FA:g}$",
        transform=ax.transAxes,
        ha="left",
        va="top",
    )

    ax = axes[1]
    ax.plot(offset_bins, response_db, color="#194c80", linewidth=1.8)
    ax.axvline(-0.5, color="#777777", linestyle="--", linewidth=0.9)
    ax.axvline(0.5, color="#777777", linestyle="--", linewidth=0.9)
    ax.axhline(half_bin_loss, color="#b4462a", linestyle=":", linewidth=1.2)
    ax.scatter([0.5], [half_bin_loss], color="#b4462a", s=18, zorder=3)
    ax.annotate(
        f"half-bin loss = {half_bin_loss:.2f} dB",
        xy=(0.5, half_bin_loss),
        xytext=(0.62, -1.1),
        arrowprops={"arrowstyle": "->", "color": "#555555", "lw": 0.8},
    )
    ax.set_xlabel("Tone offset from tested bin (DFT bins)")
    ax.set_ylabel("Normalized output (dB)")
    ax.set_title("(b) A DFT bin is only one matched filter")
    ax.set_ylim(-30, 1)
    ax.set_xlim(-1.5, 1.5)
    ax.grid(True, alpha=0.28)

    out_dir = Path(__file__).resolve().parent
    for suffix in ("pdf", "png"):
        fig.savefig(out_dir / f"equivalence_simulation.{suffix}", dpi=300)
    print(f"maximum direct identity error: {max_identity_error:.3e}")
    print(f"half-bin loss: {half_bin_loss:.3f} dB")


if __name__ == "__main__":
    main()
