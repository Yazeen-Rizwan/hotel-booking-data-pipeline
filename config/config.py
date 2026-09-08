API_URL = "http://127.0.0.1:5000/bookings"

KAFKA_BROKER = "127.0.0.1:9092"
KAFKA_TOPIC = "hotel_bookings_live"

STAGING_FILE = "staging/staging.csv"
ERROR_LOG = "logs/error_log.csv"

FINAL_DATA = "warehouse/final_bookings.csv"
BACKUP_DATA = "warehouse/backup_bookings.csv"

REQUIRED_COLUMNS = [
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