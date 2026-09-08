import json
import requests
from kafka import KafkaProducer
from config.config import API_URL, KAFKA_BROKER, KAFKA_TOPIC


print("Starting Kafka Producer...")

# -----------------------------------------
# Connect to Kafka
# -----------------------------------------

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("Connected to Kafka.")


# -----------------------------------------
# Get bookings from Flask API
# -----------------------------------------

response = requests.get(
    API_URL,
    params={"page": 1194, "limit": 100},
    timeout=10
)


if response.status_code != 200:
    print("Failed to fetch data from Flask API.")
    print("Status:", response.status_code)
    producer.close()
    exit(1)


records = response.json()

print(f"Records received from API: {len(records)}")


# -----------------------------------------
# Send ONLY the latest booking
# -----------------------------------------

if records:

    latest_record = records[-1]

    producer.send(
        KAFKA_TOPIC,
        latest_record
    )

    producer.flush()

    print("Latest booking sent to Kafka.")
    print("Booking:")
    print(json.dumps(latest_record, indent=2))

else:
    print("No booking records received.")


producer.close()

print("Kafka Producer completed.")