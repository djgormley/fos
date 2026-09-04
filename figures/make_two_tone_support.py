"""Generate the exact two-tone cyclic-support figure used by the manuscript."""

from pathlib import Path

import matplotlib.pyplot as plt


OUTPUT = Path(__file__).with_name("two_tone_support.pdf")
DEEP_BLUE = "#194C80"
TEAL = "#197278"
BURNT_ORANGE = "#A44A1F"

ROWS = (
    (
        r"$|\widehat M_x^{k/16}|$",
        {1: 1.0, 5: 0.5},
        {1: r"$1$", 5: r"$1/2$"},
        "first-order lines",
        DEEP_BLUE,
        1.30,
    ),
    (
        r"$|\widehat R_{xx^*}^{k/16}(0)|$",
        {0: 1.25, 4: 0.5, 12: 0.5},
        {0: r"$5/4$", 4: r"$1/2$", 12: r"$1/2$"},
        "pairwise differences",
        TEAL,
        1.55,
    ),
    (
        r"$|\widehat R_{xx}^{k/16}(0)|$",
        {2: 1.0, 6: 1.0, 10: 0.25},
        {2: r"$1$", 6: r"$1$", 10: r"$1/4$"},
        "pairwise sums",
        BURNT_ORANGE,
        1.30,
    ),
)


def main() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.size": 8,
            "mathtext.fontset": "stix",
            "axes.linewidth": 0.7,
            "pdf.fonttype": 42,
        }
    )

    fig, axes = plt.subplots(
        3,
        1,
        figsize=(6.5, 4.35),
        sharex=True,
        constrained_layout=True,
    )

    for axis, (ylabel, values, labels, description, color, ymax) in zip(axes, ROWS):
        bins = list(values)
        amplitudes = [values[index] for index in bins]
        markerline, stemlines, baseline = axis.stem(bins, amplitudes)
        plt.setp(markerline, marker="o", markersize=4.5, color=color)
        plt.setp(stemlines, linewidth=1.6, color=color)
        plt.setp(baseline, linewidth=0.7, color="#5B6573")

        axis.set_ylabel(ylabel)
        axis.set_xlim(-0.55, 15.55)
        axis.set_ylim(0.0, ymax)
        axis.set_yticks((0.0, 0.5, 1.0))
        axis.grid(axis="y", linewidth=0.45, color="#D8DDE3")
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
        axis.text(
            0.985,
            0.82,
            description,
            ha="right",
            va="center",
            color="#38404A",
            transform=axis.transAxes,
        )

        for index, amplitude in values.items():
            axis.annotate(
                labels[index],
                xy=(index, amplitude),
                xytext=(0, 5),
                textcoords="offset points",
                ha="center",
                va="bottom",
                color=color,
            )

    axes[-1].set_xticks(range(0, 16, 2))
    axes[-1].set_xlabel(r"Cycle-frequency bin $k$ ($\alpha=k/16$)")
    fig.savefig(OUTPUT, bbox_inches="tight", pad_inches=0.03)


if __name__ == "__main__":
    main()
