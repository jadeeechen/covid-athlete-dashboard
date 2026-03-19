from pathlib import Path
import pandas as pd
import numpy as np


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "Athlete_Non-Athlete.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

TEMPORAL_COLUMNS = ["Survey Date"]

NUMERIC_COLUMNS_TO_COERCE = [
    "Age Group",
    "Country During Lockdown",
    "Mental Health Condition",
    "Marital Status",
    "Smoking Status",
    "Five Fruit and Veg",
    "Hours sleep",
    "Shielded",
    "Weeks Social Distancing",
    "# in lockdown bubble",
    "Athlete/Non-Athlete",
    "Psychological Wellbeing",
    "Happy",
    "HADS-A AVERAGE",
    "HADS-D AVERAGE",
    "LONE_ TOTAL",
]


def load_raw_data(file_path: Path) -> pd.DataFrame:
    return pd.read_csv(file_path, encoding="ISO-8859-1", low_memory=False)


def drop_empty_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # drop columns that are entirely empty or unnamed trailing junk columns
    unnamed_cols = [col for col in df.columns if str(col).startswith("Unnamed")]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)

    df = df.dropna(axis=1, how="all")
    return df


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.replace(r"[?:]+$", "", regex=True)
    )

    return df


def coerce_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    for column_name in NUMERIC_COLUMNS_TO_COERCE:
        if column_name in df.columns:
            df[column_name] = pd.to_numeric(df[column_name], errors="coerce")

    return df


def convert_temporal_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    for column_name in TEMPORAL_COLUMNS:
        if column_name in df.columns:
            df[column_name] = pd.to_datetime(
                df[column_name],
                dayfirst=True,
                errors="coerce"
            )

    return df


def replace_missing_codes(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # replace common missing-code variants seen in this dataset
    df = df.replace(
        {
            999: np.nan,
            999.0: np.nan,
            999.00: np.nan,
            "999": np.nan,
            "999.0": np.nan,
            "999.00": np.nan,
        }
    )

    return df


def map_base_labels(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "Gender" in df.columns:
        df["Gender"] = df["Gender"].replace({1: "Male", 2: "Female"})

    if "Athlete/Non-Athlete" in df.columns:
        df["Athlete/Non-Athlete"] = df["Athlete/Non-Athlete"].replace(
            {1: "Athlete", 2: "Non-Athlete"}
        )

    return df


def build_dashboard_base_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    data = df.copy()

    data3 = data.rename(columns={"Athlete/Non-Athlete": "is_athlete"})
    data4 = data3.copy()

    # remove spaces from headers to match downstream chart scripts
    data4.columns = data4.columns.str.replace(" ", "", regex=False)

    if "AgeGroup" in data4.columns:
        data4["AgeGroup"] = data4["AgeGroup"].replace(
            {
                1: "18-20",
                2: "21-30",
                3: "31-40",
                4: "41-50",
                5: "51-60",
                6: "61-70",
                7: "71+",
            }
        )

    if "CountryDuringLockdown" in data4.columns:
        data4["CountryDuringLockdown"] = data4["CountryDuringLockdown"].replace(
            {
                1: "UK",
                2: "Ireland",
                3: "New Zealand",
                4: "Australia",
                5: "Thailand",
                6: "Belgium",
                7: "Sweden",
            }
        )

    if "MaritalStatus" in data4.columns:
        data4["MaritalStatus"] = data4["MaritalStatus"].replace(
            {
                1: "Single",
                2: "Married/Cohabiting",
                3: "Civil Partnership",
                4: "Divorced",
                5: "Widowed",
            }
        )

    if "SmokingStatus" in data4.columns:
        data4["SmokingStatus"] = data4["SmokingStatus"].replace(
            {
                1: "Never",
                2: "Ex-occasional smoker",
                3: "Ex-smoker",
                4: "Occasional",
                5: "Half pack daily",
                6: "Full pack daily",
                7: "Multiple packs daily",
            }
        )

    if "FiveFruitandVeg" in data4.columns:
        data4["FiveFruitandVeg"] = data4["FiveFruitandVeg"].replace(
            {
                1: "Yes",
                2: "No",
            }
        )

    # remove obviously bad / corrupted psychological wellbeing rows from original workflow
    if "PsychologicalWellbeing" in data4.columns:
        data4 = data4[data4["PsychologicalWellbeing"] != 5994]

    if "Hourssleep" in data4.columns:
        data4["Hourssleep"] = pd.to_numeric(data4["Hourssleep"], errors="coerce")
        data4["Hourssleep"] = data4["Hourssleep"].replace(
            dict.fromkeys([1, 1.5, 2, 2.5, 3, 3.5], "< 4")
        ).replace(
            dict.fromkeys([4, 4.5, 5, 5.5], "< 6")
        ).replace(
            dict.fromkeys([6, 6.5, 7, 7.5], "< 8")
        ).replace(
            dict.fromkeys([8, 8.5, 9, 9.5], "< 10")
        ).replace(
            dict.fromkeys([10, 10.5], "10+")
        )

    if "WeeksSocialDistancing" in data4.columns:
        data4["WeeksSocialDistancing"] = pd.to_numeric(
            data4["WeeksSocialDistancing"],
            errors="coerce"
        )
        data4["WeeksSocialDistancing"] = data4["WeeksSocialDistancing"].replace(
            {0: 1, 2: 4, 3: 7, 4: 10, 5: 13, 6: 16, 7: 19, 8: 21}
        )

    return data3, data4


def build_happiness_by_occupation(data3: pd.DataFrame) -> pd.DataFrame:
    filtered_data = data3[data3["is_athlete"].isin(["Athlete", "Non-Athlete"])].copy()
    filtered_data["Occupation"] = filtered_data["Occupation"].astype(str).str.upper()

    grouped_occupation_data = (
        filtered_data.groupby(["Occupation", "is_athlete"], dropna=False)["Happy"]
        .mean()
        .reset_index()
    )

    grouped_occupation_data["Happy"] = grouped_occupation_data["Happy"].apply(
        lambda x: np.nan if pd.isna(x) else round(x * 4) / 4
    )

    pivot_occupation_data = grouped_occupation_data.pivot(
        index="Occupation",
        columns="is_athlete",
        values="Happy",
    )

    occupation_df = pivot_occupation_data.reset_index().dropna()

    occupation_coordinate_df = pd.DataFrame(
        {
            "y": occupation_df["Occupation"],
            "Athlete": occupation_df["Athlete"],
            "Non-Athlete": occupation_df["Non-Athlete"],
            "x1": occupation_df[["Athlete", "Non-Athlete"]].min(axis=1),
            "x2": occupation_df[["Athlete", "Non-Athlete"]].max(axis=1),
            "Difference": occupation_df["Athlete"] - occupation_df["Non-Athlete"],
        }
    )

    return occupation_coordinate_df


def map_severity(score):
    if pd.isna(score):
        return np.nan
    if score <= 7:
        return "Normal"
    if score <= 10:
        return "Mild"
    return "Severe"


def build_happiness_anxiety_depression(data4: pd.DataFrame) -> pd.DataFrame:
    data_viz2 = data4.copy()

    data_viz2["HADS-AAVERAGE"] = pd.to_numeric(data_viz2["HADS-AAVERAGE"], errors="coerce")
    data_viz2["HADS-DAVERAGE"] = pd.to_numeric(data_viz2["HADS-DAVERAGE"], errors="coerce")

    data_viz2["Anxiety Severity"] = data_viz2["HADS-AAVERAGE"].apply(map_severity)
    data_viz2["Depression Severity"] = data_viz2["HADS-DAVERAGE"].apply(map_severity)

    return data_viz2


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    df = load_raw_data(RAW_DATA_PATH)
    df = drop_empty_columns(df)
    df = clean_column_names(df)
    df = coerce_numeric_columns(df)
    df = convert_temporal_columns(df)
    df = replace_missing_codes(df)
    df = map_base_labels(df)

    data3, data4 = build_dashboard_base_data(df)

    happiness_by_occupation = build_happiness_by_occupation(data3)
    happiness_anxiety_depression = build_happiness_anxiety_depression(data4)
    dashboard_base_data = data4.copy()

    happiness_by_occupation_path = PROCESSED_DIR / "happiness_by_occupation.csv"
    happiness_anxiety_depression_path = PROCESSED_DIR / "happiness_anxiety_depression.csv"
    dashboard_base_data_path = PROCESSED_DIR / "dashboard_base_data.csv"

    happiness_by_occupation.to_csv(happiness_by_occupation_path, index=False)
    happiness_anxiety_depression.to_csv(happiness_anxiety_depression_path, index=False)
    dashboard_base_data.to_csv(dashboard_base_data_path, index=False)

    print(f"saved: {happiness_by_occupation_path}")
    print(f"rows: {len(happiness_by_occupation)}")

    print(f"saved: {happiness_anxiety_depression_path}")
    print(f"rows: {len(happiness_anxiety_depression)}")

    print(f"saved: {dashboard_base_data_path}")
    print(f"rows: {len(dashboard_base_data)}")
    print(f"columns: {len(dashboard_base_data.columns)}")


if __name__ == "__main__":
    main()