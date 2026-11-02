import json
import unittest
from aws_functions.health.lambda_function import lambda_handler


class TestHealth(unittest.TestCase):
    def test_health_response(self):
        response = lambda_handler({}, None)
        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertEqual(body["status"], "ok")
        self.assertEqual(body["service"], "agripulse-cloud")
