"""Verify the finite-record identity and plot the shared grid-mismatch curve."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


SEED = 20260902
N = 64


def main() -> None:
    rng = np.random.default_rng(SEED)
    alpha = 11 / N
    n = np.arange(N)
    s = np.exp(-1j * 2 * np.pi * alpha * n)

    # Verify the complex-valued identity on arbitrary finite records:
    # conj(M_hat(alpha)) = X_N(-alpha)/N = s_{-alpha}^H x / N.
    check_records = 4_000
    x = (
        rng.standard_normal((check_records, N))
        + 1j * rng.standard_normal((check_records, N))
    )
    cyclic_mean = np.mean(
        np.conj(x) * np.exp(-1j * 2 * np.pi * alpha * n)[None, :],
        axis=1,
    )
    matched_projection = (x @ np.conj(s)) / N
    max_identity_error = np.max(
        np.abs(np.conj(cyclic_mean) - matched_projection)
    )
    if max_identity_error > 5e-12:
        raise RuntimeError(f"Identity check failed: {max_identity_error:g}")

    # Evaluate the rectangular-window response when only one transform bin is
    # used for a tone at a nearby frequency.
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
        }
    )
    fig, ax = plt.subplots(figsize=(4.65, 2.8), constrained_layout=True)
    ax.plot(offset_bins, response_db, color="#194c80", linewidth=1.8)
    ax.axvline(-0.5, color="#777777", linestyle="--", linewidth=0.9)
    ax.axvline(0.5, color="#777777", linestyle="--", linewidth=0.9)
    ax.axhline(half_bin_loss, color="#b4462a", linestyle=":", linewidth=1.2)
    ax.scatter([0.5], [half_bin_loss], color="#b4462a", s=18, zorder=3)
    ax.annotate(
        f"Half-bin loss = {half_bin_loss:.2f} dB",
        xy=(0.5, half_bin_loss),
        xytext=(0.64, -1.25),
        arrowprops={"arrowstyle": "->", "color": "#555555", "lw": 0.8},
    )
    ax.set_xlabel("Tone offset from evaluated bin (bins)")
    ax.set_ylabel("Normalized output power (dB)")
    ax.set_title(f"Rectangular-window single-bin mismatch ($N={N}$)")
    ax.set_ylim(-30, 1)
    ax.set_xlim(-1.5, 1.5)
    ax.grid(True, alpha=0.28)

    out_dir = Path(__file__).resolve().parent
    for suffix in ("pdf", "png"):
        fig.savefig(out_dir / f"equivalence_simulation.{suffix}", dpi=300)
    print(f"maximum complex identity error: {max_identity_error:.3e}")
    print(f"half-bin loss: {half_bin_loss:.3f} dB")


if __name__ == "__main__":
    main()
