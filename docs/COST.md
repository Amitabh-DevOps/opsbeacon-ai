# OpsBeacon AI - Cost Estimation Guide

This document outlines the monthly operational costs for running **OpsBeacon AI** on AWS. The architecture is designed to stay within the **AWS Free Tier** wherever possible, utilizing highly economical serverless services.

---

## Cost Breakdown by AWS Service

OpsBeacon AI runs once per day at 8:00 AM UTC (30 times per month). Below is the calculated cost for each service based on standard AWS pricing (US East - N. Virginia).

### 1. AWS Lambda
* **Pricing Model**: $0.20 per million requests + $0.0000166667 per GB-second of execution.
* **AWS Free Tier**: 1 million free requests per month + 400,000 GB-seconds.
* **OpsBeacon Consumption**: 30 requests/month. Average execution time is 10 seconds at 256 MB memory = 2.5 GB-seconds per request.
* **Total GB-Seconds**: 30 * 2.5 = 75 GB-seconds.
* **Lambda Cost**: **$0.00** (100% covered by AWS Free Tier).

### 2. Amazon EventBridge Scheduler
* **Pricing Model**: $1.00 per million trigger executions.
* **AWS Free Tier**: 14 million trigger invocations are free per month.
* **OpsBeacon Consumption**: 30 triggers/month.
* **Scheduler Cost**: **$0.00** (100% covered by AWS Free Tier).

### 3. Amazon Bedrock (Nova Lite)
* **Model ID**: `amazon.nova-lite-v1:0`
* **Pricing Model**:
  * **Input Tokens**: $0.00006 per 1,000 tokens ($0.06 per million tokens).
  * **Output Tokens**: $0.00024 per 1,000 tokens ($0.24 per million tokens).
* **OpsBeacon Consumption**:
  * Input tokens (Prompt containing scraped RSS summaries): ~3,000 tokens per run.
  * Output tokens (Structured JSON digest): ~1,000 tokens per run.
* **Calculated Cost per Run**:
  * Input: `(3,000 / 1,000) * $0.00006 = $0.00018`
  * Output: `(1,000 / 1,000) * $0.00024 = $0.00024`
  * Total per run: `$0.00042`
* **Monthly Cost**: `30 * $0.00042 = $0.0126`
* **Bedrock Cost**: **$0.013** (under 2 cents).

### 4. Amazon SES
* **Pricing Model**: $0.10 per 1,000 emails sent.
* **AWS Free Tier**: 3,000 free messages per month (first 12 months for new accounts).
* **OpsBeacon Consumption**: 30 emails/month.
* **SES Cost**: **$0.00** (covered by AWS Free Tier) or **$0.003** (if outside Free Tier limits).

### 5. Amazon CloudWatch Logs
* **Pricing Model**: $0.50 per GB of ingested data.
* **AWS Free Tier**: 5 GB of free data ingestion per month.
* **OpsBeacon Consumption**: 30 runs * ~5 KB logs per run = 150 KB/month.
* **CloudWatch Cost**: **$0.00** (100% covered by AWS Free Tier).

---

## Monthly Summary Estimate

| AWS Service | Unit Consumption | Free Tier Eligibility | Estimated Cost (USD) |
| ----------- | ---------------- | --------------------- | -------------------- |
| **AWS Lambda** | 30 requests / 75 GB-sec | Eligible | $0.0000 |
| **EventBridge Scheduler** | 30 triggers | Eligible | $0.0000 |
| **Amazon Bedrock** | 90,000 Input / 30,000 Output | No (No standard FT) | $0.0126 |
| **Amazon SES** | 30 emails | Eligible | $0.0000 |
| **CloudWatch Logs** | ~150 KB data | Eligible | $0.0000 |
| **Total Monthly Cost** | | | **$0.0126 (approx. $0.01)** |

> [!TIP]
> OpsBeacon AI is extremely friendly to personal portfolios or developer weekend challenges, costing **less than $0.02 per month** to run.
