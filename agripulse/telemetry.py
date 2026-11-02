"""Contract validation for agriculture sensor telemetry. Standard library only."""
from __future__ import annotations

from datetime import datetime, timedelta
import math
import re
from typing import Any, Mapping
from uuid import UUID

REQUIRED = (
    "schema_version", "event_id", "site_id", "device_id", "timestamp",
    "source", "soil_moisture_pct", "temperature_c", "relative_humidity_pct",
    "rainfall_mm", "battery_pct",
)
BOUNDS = {
    "soil_moisture_pct": (0.0, 100.0),
    "temperature_c": (-30.0, 70.0),
    "relative_humidity_pct": (0.0, 100.0),
    "rainfall_mm": (0.0, 500.0),
    "battery_pct": (0.0, 100.0),
}
IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{1,63}$")


class InvalidTelemetry(ValueError):
    """Raised when a sensor payload violates the telemetry contract."""


def validate_telemetry(reading: Mapping[str, Any]) -> dict[str, Any]:
    """Validate an event and return a defensive copy.

    Does not claim synthetic inputs represent ground-truth measurements.
    """
    if not isinstance(reading, Mapping):
        raise InvalidTelemetry("Reading must be a JSON object")

    missing = sorted(set(REQUIRED) - set(reading))
    extra = sorted(set(reading) - set(REQUIRED))
    if missing or extra:
        raise InvalidTelemetry(f"Missing fields: {missing}; unknown fields: {extra}")

    if reading["schema_version"] != "1.0":
        raise InvalidTelemetry("Unsupported schema_version")
    try:
        UUID(str(reading["event_id"]))
    except (TypeError, ValueError, AttributeError) as exc:
        raise InvalidTelemetry("event_id must be a UUID") from exc

    for field in ("site_id", "device_id"):
        if not isinstance(reading[field], str) or not IDENTIFIER.fullmatch(reading[field]):
            raise InvalidTelemetry(f"Invalid {field}")

    if reading["source"] not in ("simulated", "measured"):
        raise InvalidTelemetry("source must be simulated or measured")

    timestamp = reading["timestamp"]
    if not isinstance(timestamp, str) or not timestamp.endswith("Z"):
        raise InvalidTelemetry("timestamp must be an ISO 8601 UTC string ending in Z")
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise InvalidTelemetry("Invalid timestamp") from exc
    if parsed.utcoffset() != timedelta(0):
        raise InvalidTelemetry("timestamp must be UTC")

    for field, (low, high) in BOUNDS.items():
        value = reading[field]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise InvalidTelemetry(f"{field} must be numeric")
        if not math.isfinite(value) or not low <= value <= high:
            raise InvalidTelemetry(f"{field} out of allowed range [{low}, {high}]")

    return dict(reading)
