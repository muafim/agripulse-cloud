# AgriPulse Cloud 🌱

**Cloud-Native Smart Agriculture Analytics & Predictive Irrigation Platform**

> Status: Milestone 1 (foundation) — local sensor simulator, strict schema validation,
> offline unit tests, GitHub Actions CI, and a simple AWS Lambda health-check function.
> This repository does **not** yet claim a deployed data pipeline, trained model, or live sensor data.

## Goals
- Collect agriculture telemetry reliably and distinguish measured vs simulated data.
- Run cloud-native ingestion, DynamoDB current state, and historical data lake in S3.
- Offer secure APIs and a React visualization.
- Train and evaluate a temporal moisture-prediction model using genuine reference datasets.
- Deploy repeatably with Infrastructure as Code; monitor both reliability and cost.

## Project structure
```text
agripulse/
  simulator.py          # deterministic synthetic events
  telemetry.py          # input contract validation
aws_functions/health/
  lambda_function.py    # initial Lambda console deployment
infra/                  # IaC in milestone 2
tests/                  # standard-library unit tests
data/examples/          # sample synthetic .jsonl
.github/workflows/ci.yml
 docs/                   # architecture, ADRs, cost guardrails
```

## Local run on Windows PowerShell
Requirements: Python 3.12+ and Git. No third-party Python dependencies for milestone 1.

```powershell
cd agripulse-cloud-starter
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m agripulse.simulator --devices 3 --samples-per-device 4 --seed 42 --start 2026-11-02T00:00:00Z --output data/examples/telemetry.jsonl
Get-Content data/examples/telemetry.jsonl -TotalCount 2
```

## Local run on Linux/macOS
```bash
python3 -m unittest discover -s tests -v
python3 -m agripulse.simulator --devices 3 --samples-per-device 4 --seed 42 --start 2026-11-02T00:00:00Z --output data/examples/telemetry.jsonl
head -n 2 data/examples/telemetry.jsonl
```

The simulator is reproducible when you provide the same seed and start time.
All generated records have `"source":"simulated"`.

## First AWS smoke test (console)
- Create the AWS project `AgriPulseCloud` and verify its region and Free Plan status.
- Navigate to AWS Lambda -> Event Functions -> Create Event Function -> Author from scratch.
- Name `agripulse-dev-health`, choose Python 3.14, x86_64. Do not add an API trigger yet.
- Paste `aws_functions/health/lambda_function.py` into the built-in `lambda_function.py` editor; Deploy.
- Use Test with event `{}`. Confirm `statusCode: 200` and `body.status == 'ok'`.
- Configuration: 128 MB memory, timeout 3 seconds, reserved concurrency 2 (if available).
- CloudWatch log group `/aws/lambda/agripulse-dev-health`: set retention to 7 days.
- If the function is no longer needed, delete it and its CloudWatch log group.

## Security notes
- Never commit API credentials, AWS access keys, GitHub tokens, sensor secrets, or `.env` files.
- Don't create public ingestion endpoints in milestone 1.
- Prefer temporary AWS CLI sessions (not long-lived access keys) when setting up later stages.
- In milestone 2, validate IAM execution roles and enforce least privilege.

## Milestones
1. [x] Local project skeleton, simulator, schema validation, unit tests, CI, health function sample.
2. [ ] AWS resource deployment and ingest pipeline.
3. [ ] Historical ETL / data catalog and quality checks.
4. [ ] Read API with authentication / authorization.
5. [ ] ML training and inference with evaluation metrics.
6. [ ] React frontend and alerts.
7. [ ] CI/CD, observability, security, and cost optimization.
8. [ ] Public demo, architecture write-up, final portfolio report.

## Reference documentation
- AWS Free Plan: https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-plans.html
- AWS new project: https://docs.aws.amazon.com/accounts/latest/reference/create-project.html
- AWS region: https://docs.aws.amazon.com/accounts/latest/reference/project-regions.html
- AWS Lambda getting started: https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html
