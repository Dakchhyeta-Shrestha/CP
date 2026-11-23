"""Run independently of Jupyter from project root:
python test_prediction.py --csv data/sample_building_data.csv
or:
python test_prediction.py --floor-dir Dataset/CU-Beams
"""
import argparse
import json
import pandas as pd
from backend.preprocessing import hourly_from_raw_floors
from backend.predict import EnergyForecaster


def main():
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--csv", help="Prepared hourly CSV: Date, building_demand, temperature, humidity, lux")
    source.add_argument("--floor-dir", help="Folder of seven floor-level CU-BEMS raw CSV files")
    parser.add_argument("--models", default="models", help="Folder holding model_metadata.json and .joblib models")
    args = parser.parse_args()
    data = pd.read_csv(args.csv) if args.csv else hourly_from_raw_floors(args.floor_dir)
    print(json.dumps(EnergyForecaster(args.models).predict_latest(data), indent=2))

if __name__ == "__main__":
    main()
