# CU-BEMS Dashboard — Plain Language and Recommendations

This version adds measured demand comparisons, accessible descriptions, and rule-based recommendations to the existing interactive dashboard. It uses the same four saved LightGBM model files (not included).

## Installation
Extract this ZIP into your PROJECT root. You will get `CP_Deployment_Backend/` and `frontend/` directories. Replace older copies of those directories with these. Keep `models/` and `Dataset/` unchanged.

## Run (from PROJECT root)

Terminal 1:
`python -m uvicorn backend.api:app --app-dir CP_Deployment_Backend --host 127.0.0.1 --port 8000`

Terminal 2:
`python -m http.server 5173 --directory frontend`

Open http://127.0.0.1:5173 and click Run demo forecast.

The page now shows plain-language insights, measured demand changes versus yesterday, warnings about missing data, holiday context, and suggested operational checks. All suggestions are advisory, not device-control instructions. The backend requires real model files and compatible CU-BEMS data.

**Note:** For older Python 3.9 versions, the `api.py` model fields use `Optional[str]`.
