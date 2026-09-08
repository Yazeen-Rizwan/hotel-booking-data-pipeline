from flask import Flask, jsonify, request
import pandas as pd
import os
import requests

app = Flask(__name__)

DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "hotel_bookings.csv"
)


# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

try:
    df = pd.read_csv(DATA_FILE)
    df = df.where(pd.notnull(df), None)
    print(f"Dataset loaded successfully. Rows: {len(df)}")

except Exception as e:
    print("Error loading dataset:", e)
    df = pd.DataFrame()


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.route("/")
def home():
    return jsonify({
        "status": "Running",
        "message": "Hotel Booking REST API",
        "dataset": "Hotel Booking Demand",
        "total_records": len(df)
    })


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.route("/health")
def health():
    return jsonify({
        "status": "Healthy",
        "records_loaded": len(df)
    })


# --------------------------------------------------
# Count
# --------------------------------------------------

@app.route("/count")
def count():
    return jsonify({
        "total_records": len(df)
    })


# --------------------------------------------------
# Get Bookings
# --------------------------------------------------

@app.route("/bookings", methods=["GET"])
def bookings():

    page = request.args.get(
        "page",
        default=1,
        type=int
    )

    limit = request.args.get(
        "limit",
        default=100,
        type=int
    )

    start = (page - 1) * limit
    end = start + limit

    records = df.iloc[start:end].to_dict(
        orient="records"
    )

    return jsonify(records)


# --------------------------------------------------
# Add New Booking
# --------------------------------------------------

@app.route("/bookings", methods=["POST"])
def add_booking():

    global df

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No booking data received"
            }), 400

        # Required fields
        required_fields = [
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

        # Check required fields
        missing = [
            field
            for field in required_fields
            if field not in data
        ]

        if missing:

            return jsonify({
                "error": "Missing fields",
                "fields": missing
            }), 400

        # Add missing columns required by dashboard
        data.setdefault("is_canceled", 0)
        data.setdefault("market_segment", "Direct")

        # Add new record
        new_record = pd.DataFrame([data])

        # Append to existing dataframe
        df = pd.concat(
            [df, new_record],
            ignore_index=True
        )

        # Save updated source dataset
        df.to_csv(
            DATA_FILE,
            index=False
        )

        print(
            f"New booking added. Total records: {len(df)}"
        )

        return jsonify({
            "status": "success",
            "message": "Booking added to source dataset",
            "record": data,
            "total_records": len(df)
        }), 201

    except Exception as e:

        print("Error adding booking:", e)

        return jsonify({
            "error": str(e)
        }), 500


# --------------------------------------------------
# Single Booking
# --------------------------------------------------

@app.route("/bookings/<int:index>")
def booking(index):

    if index < 0 or index >= len(df):

        return jsonify({
            "error": "Record not found"
        }), 404

    return jsonify(
        df.iloc[index].to_dict()
    )


# --------------------------------------------------
# Run Application
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )