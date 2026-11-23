# Reliable Multi-Horizon Smart Building Energy Demand Forecasting

**Final project | Computer Programming for Data Science and Artificial Intelligence | Asian Institute of Technology (AIT), November 2026**

**Team:** Aung San Lin (st126669) and Dakchhyeta Bade Shrestha (st126671)  
**Group:** Whatever It's Okay  
**Instructor:** Dr. Chantri Polprasert

## Overview

Electricity use in a university building changes with class schedules, occupancy, weekends and holidays. This project forecasts **building electricity demand 1, 6, 12 and 24 hours ahead**, examines when forecasts become less reliable, and presents the results in a browser-based dashboard intended to help building managers make informed operational decisions.

The primary model is **LightGBM**. Predictions are in **kW (power demand)**, not kWh (energy consumed). The dashboard is a **research prototype**: its recommendations are advisory and it has not demonstrated measured energy savings.

## Research questions and datasets

| Dataset | Context | Role in the project |
|---|---|---|
| **CU-BEMS (2019)** | Hourly building-demand analysis derived from minute-level sensor readings across seven floors of a university building in Bangkok | Main multi-horizon forecasting, missing-history analysis and Thai holiday experiment |
| **Appliances Energy Prediction** | Belgian household electricity demand and indoor/outdoor environmental readings | Environmental-feature ablation study |
| **Building Sites Power Consumption** | 89 candidate sites; 49 retained following data-quality screening | Generalisation to previously unseen buildings |

The datasets were **analysed separately**, not pooled as if they measured the same building or operating conditions.

## Approach

1. Explore and clean the datasets, following their respective measurement and data-quality rules.
2. Build historical-demand, calendar and—where applicable—environmental features.
3. Compare persistence, previous-day and previous-week baselines, Linear Regression, and LightGBM.
4. Train **separate direct LightGBM models** for 1h, 6h, 12h and 24h horizons.
5. Evaluate chronologically using metrics including MAE, RMSE, R², nMAE and CV(RMSE).
6. Investigate environmental features, naturally incomplete recent history, Thai holidays and transfer to unseen buildings.

The final CU-BEMS dashboard uses **four exported LightGBM models with 25 input features per model**. The saved models and their metadata must match the inference code.

## Main findings

- **Progress-stage CU-BEMS forecasting:** LightGBM achieved lower RMSE than the previous-week baseline at all four horizons. Baseline-relative RMSE reductions were **52.3% (1h), 24.3% (6h), 5.5% (12h), and 4.5% (24h)** in that comparison.
- **Environmental feature ablation:** In the **Belgian household** experiment, adding indoor/outdoor environmental information did **not consistently improve** LightGBM forecasts. Outdoor features generally caused small increases in RMSE, and combining all environmental features did not improve the mean RMSE at any of the four horizons in the reported follow-up. These findings should not be assumed to apply unchanged to CU-BEMS.
- **Incomplete historical demand:** Compared with cases with complete recent demand history, the incomplete-history group had RMSE that was **46.9% (1h), 73.9% (6h), 127.7% (12h), and 66.5% (24h) higher**. These are **observational associations** (1,949 complete vs 61 incomplete cases per horizon), **not** estimates of the causal effect of simulated sensor failures.
- **Thai public-holiday feature:** Adding the target-date holiday indicator reduced pooled RMSE by **2.16% (1h), 48.10% (6h), 14.87% (12h), and 15.38% (24h)** in the recorded paired evaluation. At 6h, RMSE fell from **87.136 to 45.227 kW**; the real holiday calendar outperformed **10 shuffled-calendar controls**. The holiday analysis is limited to its 2019 validation period.
- **Unseen-building generalisation:** LightGBM outperformed the previous-week baseline for **47 of 49 sites at 1h**, and **48 of 49 sites** at each of 6h, 12h and 24h in the reported experiment.

**Interpretation:** Strong overall accuracy does not guarantee comparable accuracy during incomplete-data or unusual operating conditions. The experiments motivate reliability-aware forecasts, rather than proving that a particular missing-data repair technique is best.

## Dashboard features

- **2019 historical mode:** Explore real historical CU-BEMS readings, demand comparisons and four forecast horizons.
- **Simulate 2026:** Demonstrate the interface with **synthetic input data** (not actual 2026 readings or live measurements).
- **CSV upload:** Generate predictions from a prepared hourly dataset with the required columns.
- **Historical demand view:** Inspect recent patterns over selectable time windows.
- **Plain-language insights / “What to do”:** Present advisory operational checks alongside the forecasts; the application does **not** control building devices.
- **Activity Planner:** Save, view and remove manager activity notes (such as seminars) using SQLite. **Notes do not currently alter model predictions.**

## Repository layout

This example reflects the final-project folder arrangement; paths may vary if you organise the research notebooks and reports differently.

```text
Final Project/
├── CP_Energy_Dashboard/
│   ├── CP_Deployment_Backend/
│   │   ├── backend/
│   │   │   ├── api.py
│   │   │   ├── predict.py
│   │   │   ├── preprocessing.py
│   │   │   └── activities.py
│   │   └── requirements.txt
│   ├── frontend/
│   │   ├── index.html
│   │   ├── styles.css
│   │   └── app.js
│   └── simulated_data/
│       └── cu_bems_simulated_2026.csv
├── models/
│   ├── lightgbm_1h.joblib
│   ├── lightgbm_6h.joblib
│   ├── lightgbm_12h.joblib
│   ├── lightgbm_24h.joblib
│   └── model_metadata.json
├── data/                    # CU-BEMS source data, if redistribution is permitted
├── notebooks/               # Final forecasting and experiment notebooks, if included
├── reports/                 # Final report, if included
├── README.md
└── .gitignore
```

The `notebooks/` and `reports/` folders above are recommended destinations; they are **not automatically created** by the dashboard ZIP. The separate `models/` folder is required for the trained-model inference path shown below.

## Running the dashboard locally

### 1. Prerequisites

- Python 3 with `pip`
- The final `CP_Energy_Dashboard/` source directory
- All **four** trusted exported `.joblib` model files and the matching `model_metadata.json`
- CU-BEMS historical floor CSVs if you want **2019 historical mode**; the simulation mode uses the included synthetic CSV

> **Security:** Only load `.joblib` files from trusted sources. Joblib/pickle deserialization can execute arbitrary code.

### 2. Open the project directory

In Terminal, go to the parent folder containing `CP_Energy_Dashboard/` and `models/`:

```bash
cd "/path/to/Final Project"
```

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r CP_Energy_Dashboard/CP_Deployment_Backend/backend/requirements.txt
```

### 3. Start the backend

Run this **from the project root**:

```bash
export CU_BEMS_MODELS_DIR="$PWD/models"
export CU_BEMS_SIM_CSV="$PWD/CP_Energy_Dashboard/simulated_data/cu_bems_simulated_2026.csv"
# Set this to the directory containing the original CU-BEMS floor CSVs:
export CU_BEMS_DEMO_FLOOR_DIR="$PWD/data/CU-Beams"

python -m uvicorn backend.api:app \
  --app-dir CP_Energy_Dashboard/CP_Deployment_Backend \
  --host 127.0.0.1 --port 8001
```

**Adjust `CU_BEMS_DEMO_FLOOR_DIR` to the *actual* location of your CU-BEMS floor files**; the example above is not guaranteed to match every copy of the project. If you only need simulated mode, you can configure the historical dataset later.

Check the API at **http://127.0.0.1:8001/health**. A healthy response should report `models_loaded: 4`.

### 4. Start the frontend

Open **another Terminal window** in the same project root:

```bash
python3 -m http.server 5173 --directory CP_Energy_Dashboard/frontend
```

Open **http://127.0.0.1:5173** in your browser.

**Port note:** The final frontend's `app.js` targets **port 8001**. Some earlier copies of the backend README use port 8000; use the matching port for the version of `app.js` in this repository.

### 5. Using CSV upload

The backend's `/predict/upload` endpoint expects an **hourly** CSV containing:

```text
Date,building_demand,temperature,humidity,lux
```

The input needs sufficient prior history to build lag features (the project uses a lag as long as 168 hours). Missing historical demand values must **not** be replaced with zero solely to make the file pass validation.

## Known limitations

- Strict CU-BEMS data-quality rules resulted in a substantial amount of missing building-demand data in 2019.
- The missing-history results compare naturally different groups and do **not** test controlled outages or establish whether filling, dropping or retaining missing values is best.
- Household environmental-feature results may not generalise to a university building.
- Holiday gains require evaluation across additional years/seasons.
- The backend reproduces the saved models' feature-generation behavior; a future retraining study should explicitly examine regularising missing hourly timestamps before lag construction.
- This is a local research prototype without production authentication or a live sensor integration. The SQLite manager notes database can contain user-entered information and should not be committed.
- Improved forecast accuracy creates **opportunities** for more efficient energy management; actual energy savings have **not** been measured.

## Future work

1. **Compare missing-data strategies** on matched evaluation windows: retain missing feature values, estimate short gaps using only information available at prediction time, or exclude incomplete periods.
2. **Simulate controlled outages** with different durations and missingness rates to measure their effects on accuracy.
3. **Improve inputs** by investigating occupancy/schedule information and building-relevant environmental features.
4. **Validate in practice** across other seasons and buildings, including studies with building managers and measured operational outcomes.

## Reproducibility and data use

The notebooks document the model-development and experimental workflows. Original dataset files may have separate licensing or redistribution requirements; include them in a public repository only when allowed. The supplied synthetic 2026 file is for demonstration, **not independent validation of forecasting accuracy**.

## License

No open-source license is asserted by this README. Add a `LICENSE` file only after the project owners agree on the terms.
