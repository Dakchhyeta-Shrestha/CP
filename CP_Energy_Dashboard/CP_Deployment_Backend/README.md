# CU-BEMS: Website backend preparation

This is the **standalone inference layer**, not yet the website/API. It follows
`01_CU_BEMS_Final_Four_Models_FIXED.ipynb`, including the original 24 inputs
and the horizon-specific **target-date** Thai holiday feature (25 total inputs).

## Where to put it

Unzip into the `PROJECT/` folder next to the existing `Dataset/` and `models/` folders.
**Keep your existing `models/` files:**

- `models/lightgbm_1h.joblib`
- `models/lightgbm_6h.joblib`
- `models/lightgbm_12h.joblib`
- `models/lightgbm_24h.joblib`
- `models/model_metadata.json`

Do **not** download/load model files from an untrusted source: joblib uses pickle.

## Install packages (from PROJECT/)

```bash
python -m pip install -r CP_Deployment_Backend/backend/requirements.txt
```

Prefer the same Python and dependency versions as those used to export your models.

## Test without Jupyter

For original raw CU-BEMS floor CSVs:

```bash
python CP_Deployment_Backend/test_prediction.py --floor-dir Dataset/CU-Beams
```

Or for an hourly CSV containing these columns:
`Date, building_demand, temperature, humidity, lux`

```bash
python CP_Deployment_Backend/test_prediction.py --csv path/to/hourly_data.csv
```

Output is JSON with four predictions, one per horizon, plus forecast timestamps.

## Important notes

- This matches the **currently exported** four models, which retain environmental
  features. If you later select a different CU-BEMS feature set, re-export models
  and metadata together before website work.
- The project currently predicts **building demand in kW**, not energy in kWh.
- The current 1h/6h/12h/24h predictors require a sufficient **hourly history**.
  The input needs at least 169 consecutive hourly rows. Missing demand hours may
  be NaN but the hourly timestamp grid must be continuous.
- Lags and rolling windows follow the notebook exactly: shift the demand column
  by 1/2/3/6/12/24/48/168 rows and compute rolling statistics from the
  **one-hour shifted** series. Missing windows are passed to LightGBM as NaN.
- The trained models used 2019 university sensor data and may not generalize to
  different buildings or later years. Their sample predictions are *not* accuracy
  guarantees. Verify time zone and sensor semantics before production use.
- Thai national holidays are not identical to the university's closure calendar.
  The `holidays` library must be installed and the date being forecast is used.
- This code does **not** automatically retrieve live data, connect a live sensor,
  create a web API, or fetch weather for the future. Raw CSV loading aggregates
  **current** temperature, humidity and illuminance from the supplied data.
- Only the notebook's 2019 model scope was evaluated; using additional years for
  input requires further validation.

## Fix for missing-hour error
Raw 2019 files are converted to an hourly timeline. Entirely missing hours are
kept as rows with NaN demand (never zero-filled), so lag/rolling features refer
to actual clock hours. If the newest available 2019 hour itself has no valid
demand, the test will report that separately rather than invent a reading.

## Handling a missing final demand reading
If the final hour has no valid `building_demand`, the predictor selects the
latest **observed** demand hour (rather than replacing it with zero). Output
includes `last_input_timestamp` and `skipped_trailing_missing_hours` so the
website can warn when the forecast origin is older than the supplied data.
The model forecasts from that older origin; it does **not** predict forward
from the missing final timestamp. It still requires at least one usable demand
lag for the chosen origin. Historical missing values remain NaN.


## Compatibility fix (training notebook vs backend)
The 2019 notebook has **8,747** rows rather than 8,760 because its
`pivot_table` omits 13 hours with no valid floor demand. Its `shift()` and
`rolling()` features were created **without restoring those missing timestamps**.
For predictions compatible with the already exported models, the backend now
reproduces this exact sparse sequence. The earlier reindexing generated large
lag differences and was removed.

This is a **compatibility fix**, not a claim that the original model training
correctly treated every lag as elapsed clock time across those three gaps.
A future methodological upgrade should regularize the time grid, recreate
future targets by timestamp, rerun evaluation and retrain models.

Run `check_backend_vs_notebook.py` from the PROJECT root to check data
feature equivalence. Minor floating point differences under 1e-5 are ignored.
Do not deploy if any material discrepancies remain.

## FastAPI — website API (new)

From your main **PROJECT** folder, install the additional API dependencies:

```bash
python -m pip install -r CP_Deployment_Backend/backend/requirements.txt
```

Start the API (it uses the four saved models in PROJECT/models):

```bash
python -m uvicorn backend.api:app --app-dir CP_Deployment_Backend --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000/docs for the interactive API test page.

- `GET /health`: verifies four models load
- `POST /predict/demo`: forecasts from the existing seven-floor CU-BEMS raw dataset
- `POST /predict/upload`: accepts a **prepared hourly CSV** with columns `Date`, `building_demand`, `temperature`, `humidity`, and `lux`. Does not accept individual raw floor CSV uploads yet.

**Important:** The demo data's latest valid forecast origin is Oct 22, 2019; API output labels this explicitly. The API is a local development service, not a production-hardened public server. Configure authentication, upload policy, CORS, HTTPS, and resource limits before public deployment. The final feature-selection comparison remains to be completed before freezing the models for submission.
