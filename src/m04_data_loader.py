from pathlib import Path
import pandas as pd


PROCESSED_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"


def load_data():
    data1 = pd.read_csv(PROCESSED_DIR / "happiness_by_occupation.csv")
    data2 = pd.read_csv(PROCESSED_DIR / "happiness_anxiety_depression.csv")
    df = pd.read_csv(PROCESSED_DIR / "dashboard_base_data.csv")
    return data1, data2, df