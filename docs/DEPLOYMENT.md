# OpsBeacon AI - Deployment Guide

This guide details the step-by-step instructions required to build, configure, and deploy **OpsBeacon AI** onto AWS.

---

## Prerequisites

Before starting, ensure you have installed and configured the following on your machine:

1. **AWS CLI** (v2) installed and configured with appropriate permissions.
2. **AWS SAM CLI** installed.
3. **Python 3.12** installed.
4. An active **AWS Account** with access to the AWS Free Tier.

---

## Step 1: Request Access to Amazon Bedrock Nova Lite

To use Bedrock models, you must explicitly enable model access in your AWS Console. OpsBeacon AI utilizes **Amazon Bedrock Nova Lite**.

1. Log in to the [AWS Management Console](https://console.aws.amazon.com/).
2. Navigate to **Amazon Bedrock**.
3. In the left navigation pane, scroll to the bottom and click on **Model access**.
4. Click **Manage model access** (top right).
5. Locate **Nova Lite** (or other desired foundation models) and check the box to request access.
6. Click **Save changes** at the bottom. The model status should change to **Access granted** within a few minutes.

<!-- IMAGE_PLACEHOLDER: Amazon Bedrock Invocation -->
*Note: Capture a screenshot of the Amazon Bedrock Model Access console page showing 'Access granted' for the Nova Lite model.*

---

## Step 2: Verify Amazon SES Identities

If your AWS account is in the **Amazon SES Sandbox** (default for new accounts), you can only send emails to and from identities (email addresses or domains) that you have explicitly verified.

1. Navigate to **Amazon Simple Email Service (SES)** in the AWS Management Console.
2. In the left panel, click **Verified identities**.
3. Click **Create identity**.
4. Select **Email address**.
5. Input your sender email address (e.g. `devops-alerts@yourdomain.com`) and click **Create identity**.
6. Check the inbox of that email address and click the verification link in the verification email sent by AWS.
7. Repeat the exact same verification steps for your recipient email address (e.g. `you@yourdomain.com`).
8. Ensure both identities show a status of **Verified** in the SES console.

<!-- IMAGE_PLACEHOLDER: SES Verified Identity -->
*Note: Capture a screenshot of the SES console showing both sender and recipient email addresses as 'Verified'.*

---

## Step 3: Build the AWS SAM Project

Run the following command to download dependencies and compile the serverless package:

```bash
sam build
```

The SAM CLI will download `feedparser`, `jinja2`, `requests`, and package them with the Python handler.

---

## Step 4: Deploy to AWS

Run the guided deployment to specify parameter configurations:

```bash
sam deploy --guided
```

You will be prompted for configurations. Use these values:

* **Stack Name**: `opsbeacon-ai`
* **AWS Region**: `us-east-1` (or your preferred region where Bedrock Nova Lite is active)
* **Parameter BedrockModelId**: `amazon.nova-lite-v1:0`
* **Parameter SenderEmail**: Your verified SES sender email (e.g., `devops-alerts@yourdomain.com`)
* **Parameter RecipientEmail**: Your verified SES recipient email (e.g., `you@yourdomain.com`)
* **Parameter RssLimit**: `5` (to keep Bedrock tokens optimal)
* **Confirm changes before deploy**: `y`
* **Allow SAM CLI IAM role creation**: `y`
* **Disable rollback**: `n`
* **Save arguments to configuration file**: `y`
* **SAM configuration file**: `samconfig.toml`
* **SAM configuration environment**: `default`

SAM will compile the IAM policies, build the Lambda function, deploy the Scheduler trigger, and setup the stack.

<!-- IMAGE_PLACEHOLDER: AWS Console Deployment -->
*Note: Capture a screenshot of the successful terminal output for 'sam deploy' showing CloudFormation resource updates.*

---

## Step 5: Verify Deployment Resources

1. Navigate to the **AWS Lambda Console** and locate `OpsBeaconAI-Engine`.
2. Navigate to the **Amazon EventBridge Console**, select **Scheduler**, and check that the schedule `OpsBeaconAI-DailyBriefingTrigger` is active.

<!-- IMAGE_PLACEHOLDER: Lambda Function -->
*Note: Capture a screenshot of the Lambda function page, showing the environment variables and permissions configuration.*

<!-- IMAGE_PLACEHOLDER: EventBridge Scheduler -->
*Note: Capture a screenshot of the Scheduler page, showing the schedule is active and targeted to the Lambda function.*

---

## Step 6: Testing the Deployment

To trigger an immediate execution instead of waiting until 8:00 AM UTC:

1. Open the **AWS Lambda Console**.
2. Open the `OpsBeaconAI-Engine` Lambda function.
3. Click the **Test** tab.
4. Keep the default empty JSON payload `{}`, name the test event `TestTrigger`, and click **Save**.
5. Click **Test** to execute the Lambda.
6. Verify the execution response shows a status of `200` with the body `OpsBeacon AI daily briefing compiled and sent successfully.`
7. Check the recipient email inbox for the daily briefing email!

<!-- IMAGE_PLACEHOLDER: Email Received -->
*Note: Capture a screenshot of the beautifully formatted HTML email received in your inbox.*

---

## Cleanup

To remove all deployed resources and prevent any AWS charges, run:

```bash
sam delete
```

Follow the prompts to confirm deletions.
