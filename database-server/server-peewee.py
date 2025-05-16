import ast
import base64
import ast
import datetime
import os
import uuid
import json
import chardet
from flask import Flask, request, jsonify
from peewee import (
    Model,
    DateTimeField,
    UUIDField,
    ForeignKeyField,
    CharField,
    IntegerField,
    BlobField,
    FloatField,
    TextField,
    SQL,
)
from playhouse.db_url import connect

try:
    import psycopg2
    from playhouse.postgres_ext import BinaryJSONField as JSONField

    DB = "postgres"
except ImportError:
    from playhouse.sqllite_ext import BinaryJSONField as JSONField

    DB = "sqlite"

app = Flask(__name__)


# Database configuration
def get_database():
    global DB
    if "DATABASE_URL" in os.environ:
        return connect(os.environ["DATABASE_URL"])

    if DB == "postgres":
        try:
            conn = connect("postgresext://postgres:postgres@localhost:5432/esp_now")
            return conn
        except:
            print("Couldn't find postgresql database, falling back to sqlite")

    DB = "sqlite"
    return connect("sqlite:///esp_now.sqlite")


database = get_database()


class BaseModel(Model):
    class Meta:
        database = database


class RawPackage(BaseModel):
    uuid = UUIDField(primary_key=True, default=uuid.uuid4)
    data = JSONField()
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])


class FallbackRecord(BaseModel):
    uuid = UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    raw_data = BlobField(null=True)
    raw_text = TextField(null=True)
    encoding = CharField(null=True)
    confidence = FloatField(null=True)
    error_message = TextField(null=True)


class Package(BaseModel):
    data_record = ForeignKeyField(RawPackage, backref="processed", on_delete="CASCADE")
    timestamp = DateTimeField(null=True)
    mac = CharField(null=True)
    rssi = IntegerField(null=True)
    remaining_data = JSONField()


# Create tables if they don't exist
with database:
    database.create_tables([RawPackage, Package, FallbackRecord], safe=True)


def process_value(value):
    """Recursively process values to convert byte-strings to base64"""
    return value

    if isinstance(value, str):
        # Handle byte strings (e.g., "b'data'")
        if value.startswith(('b"', "b'")):
            try:
                byte_value = ast.literal_eval(value)
                return base64.b64encode(byte_value).decode("utf-8")
            except (SyntaxError, ValueError):
                return value
        return value
    elif isinstance(value, dict):
        return {k: process_value(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [process_value(item) for item in value]
    return value


def log_and_save_fallback(error, status_code=400):
    """Save failed request to fallback table and log error"""
    raw_bytes = request.get_data()
    detected = chardet.detect(raw_bytes)

    try:
        raw_text = request.get_json(force=True)
    except:
        raw_text = None

    try:
        FallbackRecord.create(
            raw_data=raw_bytes,
            raw_text=raw_text,
            encoding=detected["encoding"],
            confidence=detected["confidence"],
            error_message=str(error),
        )
    except Exception as fallback_error:
        app.logger.error(f"Failed to save fallback record: {fallback_error}")

    app.logger.error(f"Request processing failed: {error}")
    return jsonify({"error": str(error)}), status_code


@app.route("/data", methods=["POST"])
def store_data():
    try:
        with database.atomic():
            # Attempt to parse JSON with encoding detection
            raw_bytes = request.get_data()
            detected = chardet.detect(raw_bytes)

            try:
                raw_data = request.get_json(force=True)
            except Exception as e:
                # Re-raise with encoding information
                raise ValueError(
                    f"JSON parsing failed (detected encoding: {detected['encoding']}, "
                    f"confidence: {detected['confidence']:.2f}): {str(e)}"
                )

            # Process and validate data
            processed_data = process_value(raw_data)
            data_record = RawPackage.create(data=processed_data)

            raw_data = json.loads(raw_data)
            # Extract fields for processed record
            timestamp = raw_data.get("timestamp")
            mac = raw_data.get("mac")
            rssi = raw_data.get("rssi")

            remaining_data = raw_data.copy()
            remaining_data.pop("timestamp", None)
            remaining_data.pop("mac", None)
            remaining_data.pop("rssi", None)

            try:
                print("a", timestamp)
                t = ast.literal_eval(timestamp)
                print("b", timestamp)
                t = *t[:3],*t[4:] # esp timestamp contains weekday
                print("c", timestamp)
                timestamp=datetime.datetime(*t)
                print("d", timestamp)
            except ValueError:
                timestamp = None
            

            # Validate and create processed record
            try:
                Package.create(
                    data_record=data_record,
                    timestamp=timestamp,
                    mac=mac,
                    rssi=rssi,
                    remaining_data=remaining_data,
                )
            except ValueError as e:
                raise ValueError(f"Field validation failed: {str(e)}")

            return jsonify({"status": "success", "uuid": str(data_record.uuid)}), 201

    except Exception as e:
        return log_and_save_fallback(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
