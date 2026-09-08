import os
import shutil
import pandas as pd
from pandas.errors import EmptyDataError
from config.config import ERROR_LOG, STAGING_FILE

print("Starting Replay Process...")

# Check if error log exists
if not os.path.exists(ERROR_LOG):

    print("No error log found.")
    print("Nothing to replay.")

else:

    try:
        error_df = pd.read_csv(ERROR_LOG)

        if error_df.empty:
            print("Error log is empty.")
            print("Nothing to replay.")

        else:
            print(f"Found {len(error_df)} error records.")

            replay_file = "replay/replayed_data.csv"

            shutil.copy(STAGING_FILE, replay_file)

            print("Replay completed successfully.")
            print(f"Replay file saved to {replay_file}")

    except EmptyDataError:

        print("Error log is empty.")
        print("Nothing to replay.")