# First-Order Cyclic Moments and Tone Matched Filtering

This repository contains the manuscript source and numerical verification for
*First-Order Cyclic Moments as Tone Matched-Filter Outputs: The Finite-Record
Identity Made Explicit*.

## Verify the identities

The verification script was tested with Python 3.12.3. Create an isolated
environment, install the pinned dependency, and run the script:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python equivalence_simulation.py
```

The script uses random seed `20260902` and checks, for seeded random complex
records and an off-grid cycle frequency, the nonconjugate and conjugate
first-order cyclic means

$$
\widehat M_x^{\alpha}
=\widehat R_{x,1}^{\alpha}(0)
=\frac{1}{N}\sum_{n=0}^{N-1}
x[n]\mathrm{e}^{-\mathrm{j}2\pi\alpha n},
$$

and

$$
\widehat M_{x^*}^{\alpha}
=\widehat R_{x^*,1}^{\alpha}(0)
=\frac{1}{N}\sum_{n=0}^{N-1}
x^*[n]\mathrm{e}^{-\mathrm{j}2\pi\alpha n}.
$$

It also checks their frequency-reflection relation

$$
\left[\widehat M_{x^*}^{\alpha}\right]^*
=\left[\widehat R_{x^*,1}^{\alpha}(0)\right]^*
=\widehat R_{x,1}^{-\alpha}(0)
=\widehat M_x^{-\alpha}.
$$

It then verifies the symmetric matched-filter identity

$$
y_{\mathrm{MF}}(f)
=N\widehat M_x^f
=N\left[\widehat M_{x^*}^{-f}\right]^*.
$$

Here $\widehat M_{x^*}^{\alpha}$ means the cyclic mean of the
conjugated sequence; it is not the conjugate of the completed coefficient
$\widehat M_x^{\alpha}$.

It also verifies that the tone inner product is the aligned output of the
conjugated, time-reversed template. A successful run reports all errors below
`5e-12`.

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
- `equivalence_simulation.py`: numerical checks for the two identities;
- `requirements.txt`: version-pinned direct Python dependency.

The exact manuscript submission should be preserved as an immutable repository
release and, when practical, archived with a persistent identifier.
