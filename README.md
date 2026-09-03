# First-Order Cyclostationarity and Tone Matched Filtering

This repository contains the manuscript source and numerical verification for
*A First-Order Cyclostationarity Statistic Reduces to Tone Matched Filtering:
An Equivalence Chain and Its Conditions*.

## Reproduce the numerical results

The figure script was tested with Python 3.12.3. Create an isolated environment,
install the pinned dependencies, and run the script:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
MPLBACKEND=Agg python equivalence_simulation.py
```

The script uses random seed `20260902` and writes:

- `equivalence_simulation.pdf`, used by the manuscript;
- `equivalence_simulation.png`, a raster preview.

A successful run reports a direct identity error below `5e-12` and a half-bin
loss of approximately:

```text
half-bin loss: -3.922 dB
```

The Monte Carlo result uses 80,000 trials, a record length of 64 samples, and
a false-alarm probability of 0.01. The script also checks the cyclic-mean and
matched-filter forms directly and raises an error if their maximum difference
exceeds `5e-12`.

## Build the manuscript

The manuscript was tested with Latexmk 4.83 and pdfTeX from TeX Live 2023. It
uses the `IEEEtran` class.

```bash
mkdir -p tmp/pdfs
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=tmp/pdfs main.tex
```

The resulting manuscript is `tmp/pdfs/main.pdf`.

## Repository contents

- `main.tex`: manuscript source;
- `equivalence_simulation.py`: numerical checks and figure-generation script;
- `equivalence_simulation.pdf`: generated figure included by the manuscript;
- `requirements.txt`: version-pinned direct Python dependencies.

The exact manuscript submission should be preserved as an immutable repository
release and, when practical, archived with a persistent identifier.
