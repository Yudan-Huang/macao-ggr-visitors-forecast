# Dash live demo — 90-second script

The presentation's M3 section includes a live Dash demo. The app is a presentation layer over the final 84-month analysis; it does not introduce a new model.

## Run

```bash
python dash_app.py
```

Open <http://127.0.0.1:8050>.

Requirements: `dash`, `plotly`, `pandas`, `numpy`, `scikit-learn` (see `requirements_dash.txt`).

## Tabs and what to show

| Tab | What it shows | One line to say |
|---|---|---|
| **Overview** | 84-month GGR + arrivals with regime shading | "2020 collapse, 2023 recovery, 2024-25 plateau — three regimes." |
| **Regimes** | GGR per 10k arrivals: 74.4 / 101.7 / 63.7 | "The same visitor count means different GGR in different regimes." |
| **Models** | Test R² / RMSE: pooled negative; 24m green; 48m blue | "Pooled fails; the validation-selected 24m is comparable to the 48m reference." |
| **Validation** | 2024 validation table, 24m highlighted | "24m has the lowest validation RMSE; 2025 was untouched." |
| **2025 test** | Predicted vs actual scatter | "0.658 / 941.6 / 832.9 — comparable, not a bigger R²." |
| **What-if** | Arrivals + month + t → predicted GGR | "Illustrative only: 350k arrivals in October gives ~22.9bn; not a forecast." |

## 90-second demo flow

1. **0:00–0:15** — Overview tab: point to 2020, 2023, 2024-25; "three regimes."
2. **0:15–0:30** — Regimes tab: 74.4 / 101.7 / 63.7; "same visitor count, different GGR."
3. **0:30–0:50** — Models tab: 24m green vs 48m blue; "pooled negative, selected model comparable."
4. **0:50–1:05** — Validation tab: "2024 validation selected 24m; 2025 untouched."
5. **1:05–1:20** — 2025 test tab: "0.658, comparable R²."
6. **1:20–1:30** — What-if tab: set 350 / Month 10 / t=75; "illustrative only."

## If the live demo fails

Use the screenshots in `presentation_assets/`:

- `dash_overview.png`
- `dash_regimes.png`
- `dash_models.png`
- `dash_whatif.png`

Say: "The app is running locally; these are the same screens from the final notebook." Do not spend time debugging in front of the class.

## Troubleshooting

- Port 8050 already in use: stop the other process, or change the last line of `dash_app.py` to another port.
- `ModuleNotFoundError: dash`: `pip install -r requirements_dash.txt`.
- The app expects `gambling_visitors_cleaned.csv` in the same folder; run from the project root.
