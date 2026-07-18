# OpsBeacon AI - Troubleshooting Guide

This guide helps resolve common errors and operational hurdles encountered when deploying and running the OpsBeacon AI agent.

---

## 1. Amazon SES Sandbox Issues

### Symptom:
`SES ClientError sending email: MessageRejected: Email address is not verified.`

### Cause:
By default, all new AWS accounts start in the SES Sandbox. While in the sandbox, you can only send emails **from** verified email addresses/domains **to** verified email addresses/domains.

### Resolution:
1. Double-check that **both** the `SENDER_EMAIL` and `RECIPIENT_EMAIL` values set in your environment variables match verified identities in your AWS SES Console.
2. Check the recipient's inbox (including the spam/junk folder) for a verification request email from Amazon SES and click the confirmation link.
3. If you want to send emails to unverified recipients, request production access for SES via the AWS Support Center.

---

## 2. Amazon Bedrock Access Denied

### Symptom:
`AccessDeniedException: You do not have access to the requested model: amazon.nova-lite-v1:0`

### Cause:
You have not activated model access for Bedrock Nova Lite in the AWS console, or you are running the agent in a region where the Nova Lite model is not available or enabled.

### Resolution:
1. Log in to the AWS Console in the region where the stack is deployed (e.g. `us-east-1`).
2. Go to **Amazon Bedrock** -> **Model access**.
3. Confirm that **Nova Lite** is checked and its status is **Access granted**.
4. If you receive permission errors from local command line execution, verify that your local AWS IAM profile has the `bedrock:InvokeModel` permission.

<!-- IMAGE_PLACEHOLDER: Amazon Bedrock Invocation -->
*Note: Look at the Bedrock Model Access page to confirm 'Access granted' for the selected model ID.*

---

## 3. EventBridge Scheduler is Not Triggering

### Symptom:
The daily briefing email is not arriving at 8:00 AM UTC, and there are no logs inside CloudWatch Logs.

### Cause:
1. The Scheduler is disabled.
2. The IAM role designated for the Scheduler does not have permission to invoke the Lambda function.
3. The cron schedule timezone is different (default is UTC).

### Resolution:
1. Go to the **EventBridge Console** -> **Schedules**.
2. Locate `OpsBeaconAI-DailyBriefingTrigger` and ensure the status is **ENABLED**.
3. Check the Scheduler's target execution role `OpsBeaconScheduleToLambdaRole` to verify it has `lambda:InvokeFunction` permission for the `OpsBeaconAI-Engine` Lambda function.
4. Verify if execution logs exist in CloudWatch. If the schedule fired but the Lambda failed, logs will show up in `/aws/lambda/OpsBeaconAI-Engine`.

<!-- IMAGE_PLACEHOLDER: EventBridge Scheduler -->
*Note: Capture a screenshot of the EventBridge Scheduler schedule details page showing the enabled status.*

---

## 4. Lambda Function Timed Out

### Symptom:
`Task timed out after 15.00 seconds` in CloudWatch Logs.

### Cause:
The default Lambda timeout is too low (e.g., 3 or 15 seconds). Fetching multiple web RSS feeds and invoking Amazon Bedrock can take between 5 to 30 seconds depending on network latency and model response length.

### Resolution:
OpsBeacon AI uses a default timeout of **300 seconds** (5 minutes) in `template.yaml`. If you modified the template or deployed manually, ensure the timeout is configured to at least 60 seconds (1 minute) to allow Bedrock to complete response generation.

---

## 5. Structured Logs are Missing Fields in CloudWatch

### Symptom:
Logs display in plain text instead of formatted JSON.

### Cause:
The system is using Python's default root logger instead of the custom structured JSON logger from `src.logger`.

### Resolution:
Ensure all files import the logger using:
```python
from src.logger import get_logger
logger = get_logger(__name__)
```
Avoid using standard `print()` statements, which are not structured as JSON, and make sure that any variables are passed using the `extra_fields` argument to keep the structured log schema consistent.

<!-- IMAGE_PLACEHOLDER: CloudWatch Logs -->
*Note: Capture a screenshot of CloudWatch Logs query results showing clean JSON logs from OpsBeacon.*
