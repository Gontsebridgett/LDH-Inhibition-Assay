"""
ldh_inhibition_analysis.py

Calculates percent inhibition of LDH activity at each inhibitor concentration
relative to the uninhibited control, and estimates IC50 by fitting a
four-parameter logistic (sigmoidal) dose-response curve.
"""

import csv
import math
from pathlib import Path

DATA_PATH = Path(__file__).parent / "sample_data" / "ldh_kinetics.csv"


def load_data(path: Path):
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append((float(row["inhibitor_uM"]), float(row["rate_a340_per_min"])))
    return rows


def percent_inhibition(rows):
    control_rate = next(rate for conc, rate in rows if conc == 0.0)
    return [(conc, rate, round((1 - rate / control_rate) * 100, 1)) for conc, rate in rows]


def logistic(x, top, bottom, ic50, hill):
    return bottom + (top - bottom) / (1 + (ic50 / x) ** hill) if x > 0 else bottom


def fit_ic50(data, top=100.0, bottom=0.0, hill=1.0, iterations=2000, lr=0.01):
    """
    Simple gradient-free grid + refinement search for IC50 (log-spaced),
    avoiding an external curve-fitting dependency (e.g. scipy) so the
    script has zero external requirements beyond the standard library.
    """
    nonzero = [(c, pct) for c, _, pct in data if c > 0]

    def sse(ic50_candidate):
        return sum((logistic(c, top, bottom, ic50_candidate, hill) - pct) ** 2 for c, pct in nonzero)

    # Coarse log-scale search
    candidates = [10 ** (e / 10) for e in range(-20, 40)]
    best = min(candidates, key=sse)

    # Local refinement around the best coarse candidate
    span = best * 0.5
    for _ in range(30):
        refined = [best + span * (i / 10 - 0.5) for i in range(21)]
        refined = [c for c in refined if c > 0]
        best = min(refined, key=sse)
        span *= 0.6

    return round(best, 2)


def main():
    rows = load_data(DATA_PATH)
    data = percent_inhibition(rows)

    print(f"{'Inhibitor (uM)':<17}{'Rate (A340/min)':<18}{'% Inhibition'}")
    print("-" * 50)
    for conc, rate, pct in data:
        print(f"{conc:<17}{rate:<18}{pct}")

    ic50 = fit_ic50(data)
    print(f"\nEstimated IC50: {ic50} uM")


if __name__ == "__main__":
    main()
