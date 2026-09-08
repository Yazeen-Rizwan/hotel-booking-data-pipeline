from unittest.mock import patch, MagicMock
import pandas as pd
import pytest

from local_pipeline import run_pipeline
from api.app import app


@pytest.fixture
def valid_booking_payload():
    return {
        "hotel": "City Hotel",
        "lead_time": 34,
        "arrival_date_year": 2026,
        "arrival_date_month": "September",
        "arrival_date_day_of_month": 8,
        "adults": 2,
        "children": 0,
        "babies": 0,
        "adr": 120.50
    }


# -----------------------------------------------------------------------------
# Pipeline Business Logic & Validation Tests (Mocked I/O)
# -----------------------------------------------------------------------------

@patch("os.makedirs")
@patch("os.path.exists")
@patch("pandas.DataFrame.to_csv")
def test_pipeline_valid_booking_mocked(mock_to_csv, mock_exists, mock_makedirs, valid_booking_payload):
    """
    Tests successful execution of run_pipeline with valid input.
    Mocking file system calls ensures tests are deterministic and isolated.
    """
    mock_exists.return_value = False  # Simulates first-time warehouse creation

    success, message = run_pipeline(valid_booking_payload)

    assert success is True
    assert "Booking processed successfully" in message
    assert mock_to_csv.call_count >= 1


def test_pipeline_missing_required_columns():
    """Validates that run_pipeline rejects input missing mandatory columns."""
    incomplete_booking = {
        "hotel": "City Hotel",
        "adults": 2
    }

    success, message = run_pipeline(incomplete_booking)

    assert success is False
    assert "Missing columns" in message


def test_pipeline_null_value_validation():
    """Validates that run_pipeline rejects input containing null values in required columns."""
    invalid_booking = {
        "hotel": "City Hotel",
        "lead_time": 10,
        "arrival_date_year": 2026,
        "arrival_date_month": "August",
        "arrival_date_day_of_month": 12,
        "adults": None,  # Invalid null
        "children": 0,
        "babies": 0,
        "adr": 100.0
    }

    success, message = run_pipeline(invalid_booking)

    assert success is False
    assert "Null value found" in message


def test_pipeline_negative_adr_validation(valid_booking_payload):
    """Validates business logic rule: ADR (Average Daily Rate) cannot be negative."""
    invalid_booking = valid_booking_payload.copy()
    invalid_booking["adr"] = -50.0

    success, message = run_pipeline(invalid_booking)

    assert success is False
    assert "ADR cannot be negative" in message


def test_pipeline_negative_adults_validation(valid_booking_payload):
    """Validates business logic rule: Adults count cannot be negative."""
    invalid_booking = valid_booking_payload.copy()
    invalid_booking["adults"] = -1

    success, message = run_pipeline(invalid_booking)

    assert success is False
    assert "Adults cannot be negative" in message


@patch("os.makedirs")
@patch("os.path.exists")
@patch("pandas.read_csv")
@patch("pandas.DataFrame.to_csv")
def test_pipeline_idempotent_deduplication(mock_to_csv, mock_read_csv, mock_exists, mock_makedirs, valid_booking_payload):
    """
    Validates idempotent behavior: duplicate incoming records are removed before saving to warehouse.
    """
    mock_exists.return_value = True

    # Existing warehouse dataframe already containing the same booking record
    existing_df = pd.DataFrame([valid_booking_payload])
    mock_read_csv.return_value = existing_df

    success, message = run_pipeline(valid_booking_payload)

    assert success is True
    assert "Booking processed successfully" in message


# -----------------------------------------------------------------------------
# API Endpoint Integration Tests (Mocked Client)
# -----------------------------------------------------------------------------

@pytest.fixture
def api_client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_api_health_endpoint(api_client):
    """Tests API /health endpoint response."""
    response = api_client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "Healthy"


def test_api_add_booking_missing_fields(api_client):
    """Tests API POST /bookings error handling when payload is missing required fields."""
    response = api_client.post("/bookings", json={"hotel": "City Hotel"})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Missing fields"
