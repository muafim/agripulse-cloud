"""Reproducible synthetic IoT events for infrastructure integration tests.

Not for claiming measured agricultural insights or ML predictive accuracy.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
import math
from pathlib import Path
import random
from uuid import NAMESPACE_URL, uuid5

from .telemetry import validate_telemetry


def make_readings(
    *,
    devices: int = 3,
    samples_per_device: int = 4,
    seed: int = 42,
    start_time: datetime | None = None,
    interval_minutes: int = 15,
) -> list[dict]:
    if devices < 1 or devices > 20:
        raise ValueError("devices must be between 1 and 20")
    if samples_per_device < 1 or samples_per_device > 10000:
        raise ValueError("samples_per_device must be between 1 and 10000")
    if interval_minutes < 1:
        raise ValueError("interval_minutes must be positive")

    base = start_time or datetime.now(timezone.utc).replace(second=0, microsecond=0)
    if base.tzinfo is None or base.utcoffset() != timedelta(0):
        raise ValueError("start_time must be timezone-aware UTC")

    rng = random.Random(seed)
    output = []
    for index in range(samples_per_device):
        when = (base + timedelta(minutes=index * interval_minutes)).isoformat(timespec="seconds").replace("+00:00", "Z")
        for device_idx in range(1, devices + 1):
            device_id = f"AGRI-{device_idx:03d}"
            rain = round(max(0.0, rng.gauss(0.2, 0.5)), 2)
            temperature = round(28 + 2 * math.sin(index / 5) + rng.uniform(-0.8, 0.8), 2)
            moisture = round(min(100.0, max(0.0, 60 - device_idx * 1.5 - index * 0.4 + rain + rng.uniform(-1, 1))), 2)
            reading = {
                "schema_version": "1.0",
                "event_id": str(uuid5(NAMESPACE_URL, f"agripulse:{seed}:{device_id}:{when}")),
                "site_id": "farm-demo",
                "device_id": device_id,
                "timestamp": when,
                "source": "simulated",
                "soil_moisture_pct": moisture,
                "temperature_c": temperature,
                "relative_humidity_pct": round(min(100.0, max(0.0, 72 + rng.uniform(-6, 6))), 2),
                "rainfall_mm": rain,
                "battery_pct": round(max(0.0, 98 - index * 0.01 - rng.uniform(0, 0.3)), 2),
            }
            output.append(validate_telemetry(reading))
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate clearly labeled synthetic agriculture sensor events")
    parser.add_argument("--devices", type=int, default=3)
    parser.add_argument("--samples-per-device", type=int, default=4)
    parser.add_argument("--interval-minutes", type=int, default=15)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--start", default=None, help="UTC ISO timestamp, e.g. 2026-11-02T00:00:00Z")
    parser.add_argument("--output", type=Path, default=Path("data/examples/telemetry.jsonl"))
    args = parser.parse_args()
    start = datetime.fromisoformat(args.start.replace("Z", "+00:00")) if args.start else None
    readings = make_readings(devices=args.devices, samples_per_device=args.samples_per_device,
                             seed=args.seed, start_time=start, interval_minutes=args.interval_minutes)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(event, separators=(",", ":")) + "\n" for event in readings), encoding="utf-8")
    print(f"Generated {len(readings)} SIMULATED events → {args.output}")


if __name__ == "__main__":
    main()
