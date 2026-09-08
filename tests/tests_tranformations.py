import pandas as pd
import pytest


def transform_booking_data(df):
    """
    Transforms raw booking data:
    - Fills missing values in key numeric columns with 0
    - Removes duplicate records
    """
    if df.empty:
        return df.copy()

    df = df.copy()

    for col in ["children", "babies", "adults", "adr"]:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    df = df.drop_duplicates()
    return df


def validate_booking_data(df):
    """
    Validates that required schema columns exist in the DataFrame.
    """
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


# -----------------------------------------------------------------------------
# Core Transformation & Schema Tests (Original Suite Preserved)
# -----------------------------------------------------------------------------

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


# -----------------------------------------------------------------------------
# Additional Academic Exercise Tests (Edge Cases, Nulls & Boundary Conditions)
# -----------------------------------------------------------------------------

def test_empty_dataframe_transformation():
    """Validates transformation behavior when input DataFrame is completely empty."""
    df = pd.DataFrame(columns=["hotel", "children", "babies", "adults", "adr"])
    result = transform_booking_data(df)
    assert len(result) == 0
    assert list(result.columns) == ["hotel", "children", "babies", "adults", "adr"]


def test_multiple_missing_numeric_fields():
    """Validates that all specified numeric columns handle nulls correctly."""
    df = pd.DataFrame({
        "hotel": ["Resort Hotel", "City Hotel"],
        "adults": [None, 1],
        "children": [1.0, None],
        "babies": [None, None],
        "adr": [None, 85.5]
    })
    result = transform_booking_data(df)

    assert result["adults"].iloc[0] == 0
    assert result["children"].iloc[1] == 0
    assert result["babies"].iloc[0] == 0
    assert result["adr"].iloc[0] == 0


def test_schema_validation_partial_missing_columns():
    """Validates schema check when only one required column is missing."""
    df = pd.DataFrame({
        "hotel": ["Resort Hotel"],
        "lead_time": [100],
        "arrival_date_year": [2026],
        "arrival_date_month": ["February"],
        "arrival_date_day_of_month": [1],
        "adults": [2],
        "children": [0],
        "babies": [0]
        # 'adr' column intentionally omitted
    })
    assert validate_booking_data(df) is False