import os
import pandas as pd

from config.config import (
    STAGING_FILE,
    FINAL_DATA,
    REQUIRED_COLUMNS
)


def run_pipeline(new_booking):

    print("====================================")
    print("STARTING HOTEL BOOKING ETL PIPELINE")
    print("====================================")

    os.makedirs("staging", exist_ok=True)
    os.makedirs("warehouse", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    # 1. Convert booking to DataFrame
    new_df = pd.DataFrame([new_booking])

    print("New booking received:")
    print(new_df)

    # 2. Schema validation
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in new_df.columns
    ]

    if missing_columns:
        return False, f"Missing columns: {missing_columns}"

    # 3. Null validation
    for column in REQUIRED_COLUMNS:
        if new_df[column].isnull().any():
            return False, f"Null value found in {column}"

    # 4. Business validation
    if new_df["adr"].iloc[0] < 0:
        return False, "ADR cannot be negative"

    if new_df["adults"].iloc[0] < 0:
        return False, "Adults cannot be negative"

    # 5. Staging
    new_df.to_csv(
        STAGING_FILE,
        index=False
    )

    print("Staging completed")

    # 6. Load existing warehouse
    if os.path.exists(FINAL_DATA):

        warehouse_df = pd.read_csv(FINAL_DATA)

        before = len(warehouse_df)

        merged_df = pd.concat(
            [warehouse_df, new_df],
            ignore_index=True
        )

        # Idempotency
        merged_df = merged_df.drop_duplicates()

        after = len(merged_df)

        duplicates_removed = (
            before + len(new_df) - after
        )

    else:

        before = 0
        merged_df = new_df
        after = len(merged_df)
        duplicates_removed = 0

    # 7. Save warehouse
    merged_df.to_csv(
        FINAL_DATA,
        index=False
    )

    print("Warehouse updated")
    print("Previous records:", before)
    print("New records:", len(new_df))
    print("Duplicates removed:", duplicates_removed)
    print("Final records:", after)

    print("====================================")
    print("ETL PIPELINE COMPLETED")
    print("====================================")

    return True, "Booking processed successfully"