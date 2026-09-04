"""Verify both first-order cyclic-mean matched-filter identities."""

import numpy as np


SEED = 20260902
N = 64
RECORDS = 4_000
TOLERANCE = 5e-12


def main() -> None:
    rng = np.random.default_rng(SEED)
    # Deliberately off the N-point transform grid: the identities do not
    # require a transform-bin shortcut.
    alpha = np.sqrt(2) / 10
    n = np.arange(N)
    x = (
        rng.standard_normal((RECORDS, N))
        + 1j * rng.standard_normal((RECORDS, N))
    )

    phase_correction = np.exp(-1j * 2 * np.pi * alpha * n)
    cyclic_mean_x = np.mean(x * phase_correction, axis=1)
    cyclic_mean_x_star = np.mean(
        np.conj(x) * phase_correction, axis=1
    )

    s_plus = np.exp(1j * 2 * np.pi * alpha * n)
    s_minus = np.exp(-1j * 2 * np.pi * alpha * n)
    matched_plus = x @ np.conj(s_plus)
    matched_minus = x @ np.conj(s_minus)

    cyclic_mean_x_error = np.max(
        np.abs(cyclic_mean_x - matched_plus / N)
    )
    cyclic_mean_x_star_error = np.max(
        np.abs(np.conj(cyclic_mean_x_star) - matched_minus / N)
    )

    cyclic_mean_x_at_minus_alpha = np.mean(
        x * np.exp(1j * 2 * np.pi * alpha * n), axis=1
    )
    cyclic_mean_reflection_error = np.max(
        np.abs(
            cyclic_mean_x_star
            - np.conj(cyclic_mean_x_at_minus_alpha)
        )
    )

    # The inner product is also the aligned convolution output of the
    # conjugated, time-reversed tone template.
    h_plus = np.conj(s_plus[::-1])
    aligned_convolution = np.array(
        [np.convolve(record, h_plus)[N - 1] for record in x]
    )
    filter_error = np.max(np.abs(aligned_convolution - matched_plus))

    errors = {
        "M_x branch": cyclic_mean_x_error,
        "M_x_star branch": cyclic_mean_x_star_error,
        "cyclic-mean reflection": cyclic_mean_reflection_error,
        "matched-filter alignment": filter_error,
    }
    for name, error in errors.items():
        if error > TOLERANCE:
            raise RuntimeError(f"{name} failed: {error:g}")
        print(f"{name} maximum error: {error:.3e}")


if __name__ == "__main__":
    main()
