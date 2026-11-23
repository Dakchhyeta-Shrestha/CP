# Restore working dashboard (V6, before Activity Planner)

This rollback restores the dashboard from before the Activity Planner and custom Gregorian calendars. It retains historical 2019 forecasts and simulated 2026 forecasting. There is no activity-save functionality in this version.

## Installation from PROJECT root
1. Stop both running servers with Ctrl+C.
2. Backup your existing `CP_Energy_Dashboard` folder.
3. Extract this ZIP in your **PROJECT** root. Its paths intentionally start with `CP_Energy_Dashboard/`. Agree to replace existing files. Do not extract into an additional nested folder.
4. Keep your existing `models/`, `Dataset/`, and `CP_Energy_Dashboard/CP_Deployment_Backend/backend/predict.py` and `preprocessing.py` intact.
5. Run the backend: `python -m uvicorn backend.api:app --app-dir CP_Energy_Dashboard/CP_Deployment_Backend --host 127.0.0.1 --port 8000`
6. In another terminal run frontend: `python -m http.server 5173 --directory CP_Energy_Dashboard/frontend`
7. Open `http://127.0.0.1:5173/?v=rollback-v6` and hard refresh (Cmd+Shift+R).

**Important:** This version does not have a working manager activity-save button. The earlier `Could not save: Not Found` arose from the V7/V8 activity API not being served/matched. Rolling back removes that feature rather than claiming it was fixed. Stored SQLite data, if any, is not deleted. The browser-native historical date input may again use the system Buddhist calendar; select AD date as supported by the browser, or use the demo mode.

2019 mode uses historical measured demand; the 2026 mode uses synthetic inputs (not real measurements).
