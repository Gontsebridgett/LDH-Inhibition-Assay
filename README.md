# Lactate Dehydrogenase (LDH) Inhibition Assay

A kinetic enzyme-inhibition assay measuring how an inhibitor reduces Lactate
Dehydrogenase (LDH) activity, paired with a Python script that calculates
percent inhibition at each inhibitor concentration and estimates the IC50
(the inhibitor concentration producing 50% inhibition) by curve fitting.

## Overview

LDH catalyses the reversible conversion of pyruvate to lactate, coupled with
the oxidation of NADH to NAD⁺. Because NADH absorbs strongly at 340 nm and
NAD⁺ does not, the rate of NADH disappearance (decrease in A340 over time) is
directly proportional to LDH activity. Adding a candidate inhibitor at
increasing concentrations and comparing the resulting reaction rate to an
uninhibited control allows calculation of percent inhibition, and fitting a
dose-response curve gives the IC50.

## Principle

- **Reaction monitored:** Pyruvate + NADH → Lactate + NAD⁺ (catalysed by LDH)
- **Readout:** Decrease in absorbance at 340 nm (NADH consumption) over time
- **Inhibition:** % Inhibition = (1 − Rate_inhibited / Rate_control) × 100
- **IC50:** Inhibitor concentration at which enzyme activity is reduced by 50%,
  estimated by fitting a sigmoidal dose-response curve to % inhibition vs.
  log(inhibitor concentration)

## Materials & Reagents

- Purified LDH enzyme (or cell lysate with LDH activity)
- Substrate solution: sodium pyruvate + NADH in phosphate buffer (pH 7.4)
- Candidate inhibitor, serially diluted across a concentration range
- UV-transparent microplate or cuvettes
- Spectrophotometer / microplate reader (340 nm)
- Temperature-controlled incubator or plate reader chamber (25–37°C)

## Method (Summary)

| Step | Action |
|---|---|
| 1 | Prepare inhibitor dilution series (e.g. 8-point, 2-fold serial dilution) |
| 2 | Pre-incubate LDH enzyme with each inhibitor concentration (5–10 min) |
| 3 | Add substrate (pyruvate + NADH) to initiate the reaction |
| 4 | Record A340 at regular time intervals (e.g. every 15–30 sec, 2–5 min total) |
| 5 | Calculate initial reaction rate (slope of A340 vs. time) for each well |
| 6 | Calculate % inhibition relative to the uninhibited (0 inhibitor) control |
| 7 | Fit a dose-response curve to estimate IC50 |

## Result Interpretation

| % Inhibition | Interpretation |
|---|---|
| ~0% | No inhibitory effect at this concentration |
| ~50% | Concentration near the IC50 |
| ~100% | Complete (or near-complete) enzyme inhibition |

A lower IC50 indicates a more potent inhibitor (less compound needed to
achieve 50% inhibition).

## Analysis Script

`ldh_inhibition_analysis.py` reads reaction rate data at each inhibitor
concentration from `sample_data/ldh_kinetics.csv`, calculates % inhibition
relative to the control, and fits a four-parameter logistic (sigmoidal)
dose-response curve to estimate IC50.

### Usage

```bash
pip install -r requirements.txt
python ldh_inhibition_analysis.py
```

### Sample output

```
Inhibitor (uM)   Rate (A340/min)   % Inhibition
------------------------------------------------
0.0              0.182             0.0
0.1              0.178             2.2
1.0              0.151             17.0
10.0             0.098             46.2
100.0            0.041             77.5
1000.0           0.012             93.4

Estimated IC50: 12.68 uM
```

## Repository Structure

```
ldh-inhibition-assay/
├── README.md
├── ldh_inhibition_analysis.py
├── requirements.txt
└── sample_data/
    └── ldh_kinetics.csv
```

## Disclaimer

Educational/portfolio project based on standard enzyme kinetics assay design;
not validated against a specific commercial LDH inhibition kit.
