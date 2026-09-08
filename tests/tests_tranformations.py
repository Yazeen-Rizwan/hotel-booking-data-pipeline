import pandas as pd


def transform_booking_data(df):

    df = df.copy()

    for col in ["children", "babies", "adults", "adr"]:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    df = df.drop_duplicates()

    return df


def validate_booking_data(df):

    required_columns = [
        "hotel",
        "lead_time",
        "arrival_date_year",
        "arrival_date_month",
        "arrival_date_day_of_month",
        "adults",
        "children",
        "babies",
        "adr"
    ]

    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    return len(missing) == 0


def test_missing_values_are_filled():

    df = pd.DataFrame({
        "hotel": ["City Hotel"],
        "adults": [2],
        "children": [None],
        "babies": [None],
        "adr": [100.0]
    })

    result = transform_booking_data(df)

    assert result["children"].iloc[0] == 0
    assert result["babies"].iloc[0] == 0


def test_duplicate_records_are_removed():

    df = pd.DataFrame({
        "hotel": ["City Hotel", "City Hotel"],
        "adults": [2, 2],
        "adr": [100.0, 100.0]
    })

    result = transform_booking_data(df)

    assert len(result) == 1


def test_valid_booking_schema():

    df = pd.DataFrame({
        "hotel": ["City Hotel"],
        "lead_time": [10],
        "arrival_date_year": [2026],
        "arrival_date_month": ["January"],
        "arrival_date_day_of_month": [15],
        "adults": [2],
        "children": [0],
        "babies": [0],
        "adr": [100.0]
    })

    assert validate_booking_data(df) is True


def test_invalid_booking_schema():

    df = pd.DataFrame({
        "hotel": ["City Hotel"],
        "adults": [2]
    })

    assert validate_booking_data(df) is False