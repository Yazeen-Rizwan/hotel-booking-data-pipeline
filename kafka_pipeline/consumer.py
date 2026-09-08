import json
import pandas as pd
from kafka import KafkaConsumer

from config.config import (
    KAFKA_BROKER,
    KAFKA_TOPIC,
    STAGING_FILE
)


print("Starting Kafka Consumer...")


# -----------------------------------------
# Connect to Kafka
# -----------------------------------------

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    consumer_timeout_ms=15000,
    value_deserializer=lambda x: json.loads(
        x.decode("utf-8")
    )
)


print("Waiting for booking message...")


records = []


# -----------------------------------------
# Read booking from Kafka
# -----------------------------------------

for message in consumer:

    records.append(message.value)

    print("Booking received from Kafka.")

    # We only need ONE new booking
    break


consumer.close()


# -----------------------------------------
# Save to staging
# -----------------------------------------

if records:

    df = pd.DataFrame(records)

    df.to_csv(
        STAGING_FILE,
        index=False
    )

    print(
        f"Saved {len(df)} booking(s) to {STAGING_FILE}"
    )

else:

    print("No messages received from Kafka.")