# OpsBeacon AI - Demo Script

This guide outlines a structured script to record a professional, **2-minute video demonstration** for your AWS Builder Center Weekend Challenge submission.

---

## Recording Checklist

* **Resolution**: 1080p (1920x1080) at 30 or 60 FPS.
* **Audio**: Clear, noise-free microphone.
* **Pre-opened Tabs**:
  1. Your GitHub repository home page.
  2. AWS Console: Lambda function page (`OpsBeaconAI-Engine`).
  3. AWS Console: EventBridge Scheduler page (`OpsBeaconAI-DailyBriefingTrigger`).
  4. AWS Console: CloudWatch Log Stream page.
  5. Your email client showing the inbox.

---

## 2-Minute Script Outline

### Part 1: Project Overview (0:00 - 0:30)
* **Visual**: Show the GitHub Repository home page.
* **What to Say**:
  > *"Hi everyone! This is my submission for the AWS Builder Center Weekend Agent Challenge: OpsBeacon AI. OpsBeacon AI is an always-on serverless DevOps intelligence agent that aggregates technical updates from AWS, Kubernetes, CNCF, and Docker feeds, uses Amazon Bedrock Nova Lite to filter and summarize them, and emails a daily digest to engineers."*
  > *"The agent runs completely unattended, triggered automatically by EventBridge Scheduler every morning at 8:00 AM UTC, helping engineers stay up to date without clicking a single button."*

### Part 2: AWS Serverless Architecture (0:30 - 1:00)
* **Visual**: Switch to the AWS EventBridge Scheduler console page, then click over to the Lambda function page.
* **What to Say**:
  > *"Here is the AWS Console. OpsBeacon is built using AWS SAM. In the EventBridge Scheduler console, we can see the active schedule. It triggers our Lambda function daily using a cron trigger."*
  > *"In the Lambda console, we see our Python 3.12 function with its environment variables. It has least-privilege IAM policies, granting permissions only to Bedrock Nova Lite, CloudWatch Logs, and verified SES identities."*

### Part 3: Live Run & Execution Logs (1:00 - 1:30)
* **Visual**: Click **Test** in the Lambda Console. Once execution succeeds, navigate to the **CloudWatch Logs** tab and show the JSON logs.
* **What to Say**:
  > *"Let's trigger the Lambda function manually to simulate the Scheduler. The execution is fast and finishes successfully. Clicking over to CloudWatch Logs, we can see the structured JSON logs. The log entries show the feeds being scraped, the connection to Bedrock Nova Lite, and the email dispatch confirmation."*

### Part 4: Reviewing the Email Output (1:30 - 2:00)
* **Visual**: Switch to your email client and open the newly received daily briefing email. Scroll through the HTML cards, source badges, "Why It Matters" callouts, and the "Brain Boost" learning cards.
* **What to Say**:
  > *"And here is the inbox. We received the daily briefing email! The layout is a fully responsive HTML email with customized source badges, summaries, and impact notes for DevOps engineers."*
  > *"At the bottom, Bedrock generated a scenario-based interview question, a hands-on mini-challenge, and a recommended topic for study based on the updates."*
  > *"OpsBeacon AI is fully autonomous, runs on the AWS Free Tier, and is ready for production. Thanks for watching!"*

---

<!-- IMAGE_PLACEHOLDER: Demo Workflow -->
*Note: Include a visual timeline diagram or workflow storyboard illustrating the demo script flow.*
