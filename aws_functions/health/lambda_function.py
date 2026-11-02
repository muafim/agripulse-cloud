"""First deployed AWS Lambda smoke-test for AgriPulse Cloud.

Handler: lambda_function.lambda_handler
No external libraries, storage, permissions, or network access required.
"""
import json
from datetime import datetime, timezone


def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "headers": {"content-type": "application/json"},
        "body": json.dumps({
            "status": "ok",
            "service": "agripulse-cloud",
            "version": "0.1.0",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }),
    }
