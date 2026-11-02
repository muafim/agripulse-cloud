import unittest
from datetime import datetime, timezone
from agripulse.simulator import make_readings
from agripulse.telemetry import InvalidTelemetry, validate_telemetry


class TestTelemetry(unittest.TestCase):
    def setUp(self):
        self.time = datetime(2026, 11, 2, tzinfo=timezone.utc)

    def test_generator_is_reproducible(self):
        a = make_readings(devices=2, samples_per_device=3, seed=99, start_time=self.time)
        b = make_readings(devices=2, samples_per_device=3, seed=99, start_time=self.time)
        self.assertEqual(a, b)
        self.assertEqual(len(a), 6)
        self.assertEqual(len({r["event_id"] for r in a}), 6)
        self.assertTrue(all(r["source"] == "simulated" for r in a))

    def test_rejects_invalid_moisture(self):
        reading = make_readings(devices=1, samples_per_device=1, start_time=self.time)[0]
        reading["soil_moisture_pct"] = 110
        with self.assertRaises(InvalidTelemetry):
            validate_telemetry(reading)

    def test_rejects_non_utc_timestamp(self):
        reading = make_readings(devices=1, samples_per_device=1, start_time=self.time)[0]
        reading["timestamp"] = "2026-11-02T07:00:00+07:00"
        with self.assertRaises(InvalidTelemetry):
            validate_telemetry(reading)

    def test_rejects_bool_numeric(self):
        reading = make_readings(devices=1, samples_per_device=1, start_time=self.time)[0]
        reading["rainfall_mm"] = True
        with self.assertRaises(InvalidTelemetry):
            validate_telemetry(reading)

    def test_rejects_unknown_fields(self):
        reading = make_readings(devices=1, samples_per_device=1, start_time=self.time)[0]
        reading["api_key"] = "never-store-secrets"
        with self.assertRaises(InvalidTelemetry):
            validate_telemetry(reading)

    def test_rejects_invalid_device_count(self):
        with self.assertRaises(ValueError):
            make_readings(devices=0)
