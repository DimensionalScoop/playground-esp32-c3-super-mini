from flask import Flask, request, jsonify
import duckdb
from datetime import datetime
import logging

app = Flask(__name__)

# Configure database
DATABASE_FILE = "esp_now_received.db"


def init_database():
    with duckdb.connect(DATABASE_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sensor_data (
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                mac VARCHAR(17),
                rssi INTEGER,
                data BLOB
            )
        """)


@app.route("/sensor-data", methods=["POST"])
def handle_sensor_data():
    # Validate request
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    # Validate required fields
    required_fields = ["mac_address", "rssi", "data"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required field"}), 400

    try:
        # Convert hex data to bytes
        data_bytes = bytes.fromhex(data["data"])
    except ValueError as e:
        return jsonify({"error": f"Invalid data format: {str(e)}"}), 400

    # Insert into database
    try:
        with duckdb.connect(DATABASE_FILE) as conn:
            result = conn.execute(
                """
                INSERT INTO sensor_data 
                (mac, rssi, data)
                VALUES (?, ?, ?)
                RETURNING timestamp
            """,
                (data["mac_address"], data["rssi"], data_bytes),
            ).fetchone()

            return jsonify(
                {"message": "Data stored successfully", "id": result[0]}
            ), 201

    except Exception as e:
        logging.error(f"Database error: {str(e)}")
        return jsonify({"error": "Failed to store data"}), 500


if __name__ == "__main__":
    init_database()
    app.run(host="localhost", port=5000, debug=True)
