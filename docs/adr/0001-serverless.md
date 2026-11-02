# ADR-0001: Serverless-first architecture

- **Status:** Accepted for initial demo
- **Context:** Portfolio needs real AWS cloud deployment with minimal idle costs.
- **Decision:** Start with Lambda, DynamoDB, S3, EventBridge, API Gateway, and CloudWatch.
- **Rationale:** Usage-based services avoid always-running VM costs, and boundaries between ingestion,
  storage, API, and ML demonstrate production architecture practices.
- **Tradeoffs:** Cold starts, per-request costs, limited computation runtime, regional service limits.
- **Future:** Sensor MQTT using IoT Core after a trusted credential design is implemented.
