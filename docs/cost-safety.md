# Free Plan budget and safety guardrails

1. Confirm project plan = Free in https://settings.aws.com -> Billing.
2. Note remaining credits and remaining days. Free Plan ends at whichever occurs first.
3. Open billing/cost management -> Budgets -> Create budget, select the correct project.
   Start with a monthly budget alert (e.g. $2 or $5) for early warnings. Alerts are not hard caps.
4. Use the one AWS region shown in Project -> Overview -> Additional Info.
5. Initially deploy only one on-demand Python Lambda health function with 128 MB and 3 seconds timeout.
6. CloudWatch Logs retention: 7 days. Avoid debug logging large data payloads and secrets.
7. Phase 2 guardrails: provisioned DynamoDB and limited reads/writes, small S3 dataset with blocked public access,
   event scheduler no faster than every 15 min initially, no public unauthenticated ingestion.
8. Reserved Lambda concurrency: optional 2 to limit runaway scaling. Do not choose provisioned concurrency.
9. Do not activate GPU, permanent ML endpoint, NAT gateway, OpenSearch Serverless, large EC2, or RDS for this demo.
10. Regularly inspect AWS Settings -> Billing -> Cost by project and backup S3 data locally prior to Free Plan expiry.
11. Cleanup: remove unused Lambda, API, event rules, storage, and CloudFormation stacks when no longer needed.

IMPORTANT: This is a usage-control checklist, not a guarantee that resources are entirely free.
Free Plan protects against being billed before upgrade, but AWS credits can still be consumed.
The AWS Settings spend limit that pauses a project is a Paid Plan feature, not a Free Plan setting.
