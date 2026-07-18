# Weekend Agent Challenge: OpsBeacon AI

**Tag:** `agents`

---

## 1. Vision & What the Agent Does

**OpsBeacon AI** is a personal, always-on AI assistant designed for cloud infrastructure engineers, site reliability engineers (SREs), and DevOps professionals. Its core vision is to eliminate the daily manual process of browsing technical blogs and release notes to find relevant updates. Instead, OpsBeacon AI runs autonomously, aggregates updates from major cloud and containerization blogs, filters out marketing filler, synthesizes technical impacts, and compiles a daily learning briefing delivered directly to the engineer's inbox.

Every morning at 8:00 AM UTC, while the user is still asleep, OpsBeacon AI wakes up, evaluates what has changed in the last 24 hours across the cloud ecosystem, uses generative AI reasoning to determine if the changes affect modern infrastructure pipelines, and sends a styled, high-priority newsletter. Crucially, the agent generates customized learning resources—such as scenario-based interview questions and hands-on challenges—ensuring that the engineer doesn't just read about updates, but continuously learns how to apply them.

---

## 2. Problem Statement

Modern software development and infrastructure management move at a breakneck pace. Cloud providers and container ecosystems release dozens of announcements daily. For instance:
* **AWS** publishes multiple announcements on the "AWS What's New" blog every single day.
* **Kubernetes** updates are spread across core blogs and minor project releases.
* **CNCF** (Cloud Native Computing Foundation) frequently releases announcements regarding incubating and graduated projects.
* **Docker** updates its container engines, desktop applications, and registry features.

An engineer trying to keep up with these sources faces two main problems:
1. **Information Overload**: A significant percentage of blog posts are marketing-focused, regional availability announcements, or corporate updates that do not impact an engineer's day-to-day work.
2. **Actionability Deficit**: Standard RSS feeds give a headline and raw description, but they do not explain *why* the update matters to a DevOps workflow or *how* it should be implemented in an active pipeline.

Without an automated parser, engineers either waste 30 minutes every morning skimming blogs or stop tracking updates altogether, risking security vulnerabilities or missing out on cost-saving features.

---

## 3. User Journey

The user journey for OpsBeacon AI requires zero active operations once the agent is deployed:

```
[Deploy once via SAM] ──> [EventBridge triggers daily] ──> [Bedrock processes data] ──> [HTML delivered to Inbox]
```

1. **Deployment Phase**: The engineer deploys the serverless stack using the AWS SAM CLI, specifying their verified sender and recipient email addresses as parameters.
2. **Quiet Monitoring**: The agent runs unattended. Every day at 8:00 AM UTC, AWS EventBridge Scheduler triggers the Lambda execution.
3. **Email Consumption**: The engineer starts their workday, opens their email client, and finds the **OpsBeacon AI Daily Briefing**. They review technical summaries, read callouts detailing operational impact, and attempt the daily hands-on challenge to expand their skills.

---

## 4. How the Agent Works

The agent's execution workflow is divided into five distinct phases, running synchronously within AWS Lambda:

1. **Triggering**: EventBridge Scheduler generates an invocation event.
2. **Ingestion**: The Lambda function fetches RSS feeds from AWS What's New, Kubernetes Blog, CNCF Blog, and Docker Blog.
3. **Filtering**: The RSS reader parses publication dates and isolates only the entries published within the last 24 hours.
4. **AI Reasoning**: The aggregated list of entries is passed to **Amazon Bedrock (Nova Lite)**. The prompt instructs Bedrock to deduplicate articles, evaluate engineering relevance, summarize them into a structured JSON payload, and formulate a DevOps interview question, a practice challenge, and a learning recommendation.
5. **Dispatch**: The Lambda function renders the JSON response into a beautiful HTML template using Jinja2 and submits it to **Amazon SES** for email delivery.

<!-- IMAGE_PLACEHOLDER: Demo Workflow -->
*Note: Capture a flow diagram illustrating this 5-stage automated execution sequence.*

---

## 5. How I Built It

OpsBeacon AI is built entirely in **Python 3.12** using the **AWS Serverless Application Model (SAM)** for resource provisioning. The application layer is modular and adheres to clean coding practices:

* **Structured Logging**: A custom JSON formatter in `src/logger.py` outputs JSON records to stdout. In AWS, these are captured by CloudWatch, enabling log query analytics.
* **Resilient RSS Parsing**: The `feedparser` library is used to read feeds. Because RSS feeds represent external network dependencies, each feed is requested within a try-except block, preventing a single offline server from breaking the entire run.
* **LLM Converse API**: We leverage the boto3 `converse` API to query Bedrock. This modern API provides unified messaging schemas, making it easy to swap models.
* **HTML Templating**: Responsive layouts are compiled using `Jinja2`. Badges are automatically assigned based on feed sources using custom CSS classes.

---

## 6. AWS Services Used

* **Amazon EventBridge Scheduler**: Triggers Lambda daily. We use Scheduler instead of classic EventBridge Rules to leverage flexible execution windows and cron schedules.
* **AWS Lambda**: Executes the Python 3.12 container environment.
* **Amazon Bedrock (Nova Lite)**: Synthesizes text data. Nova Lite is chosen for its speed, low cost, and strong performance with structured outputs.
* **Amazon SES**: Transmits the compiled HTML emails.
* **Amazon CloudWatch**: Receives structured JSON logs for security audits.
* **AWS IAM**: Enforces least-privilege access, restricting Lambda policies to Bedrock Nova Lite invocation, SES sending, and CloudWatch log streaming.

---

## 7. Architecture Overview

OpsBeacon AI leverages a decoupled serverless architecture:

<!-- IMAGE_PLACEHOLDER: Architecture Diagram -->
*Note: Embed the system architecture diagram showing EventBridge, Lambda, Bedrock, and SES.*

1. **Trigger**: EventBridge Scheduler initiates the run.
2. **Compute**: Lambda downloads external feed XML.
3. **Intelligence**: Bedrock Nova Lite parses raw summaries and returns structured JSON.
4. **Delivery**: SES sends the final email, which is received by the User.

---

## 8. Challenges

During development, I encountered and resolved three major challenges:
1. **LLM Output Structuring**: LLMs can return conversational preambles (e.g. *"Here is your JSON response..."*). To solve this, I designed a strict prompt instruction requesting Bedrock to format outputs inside a markdown ```json ``` code block, combined with a robust regex extractor in `src/bedrock_client.py` that falls back to raw text.
2. **RSS Date Standardization**: Feeds represent dates in varying formats (RFC 822 vs. ISO 8601). I wrote a parser that attempts to use feedparser's normalized `published_parsed` tuple, falling back to manual datetime parsing if the tuple is missing.
3. **SES Sandbox Constraints**: SES accounts default to a sandbox where emails can only be sent to verified addresses. The implementation includes detailed warning logs explaining SES Sandbox limits and how to verify email addresses.

<!-- IMAGE_PLACEHOLDER: SES Verified Identity -->
*Note: Capture a screenshot showing verified SES identities in the console.*

---

## 9. Lessons Learned

1. **Bedrock Nova Lite Efficiency**: Nova Lite is exceptionally cost-effective and executes rapidly. It is well-suited for automation workflows where prompt size is small to medium.
2. **Keep Prompt Lengths Optimal**: Passing full blog text to the LLM would quickly exceed context windows and raise costs. Truncating RSS descriptions before passing them to Bedrock keeps token usage minimal.
3. **Serverless Orchestration is Ideal**: Building this agent with container-based infrastructure would require continuous operational maintenance and higher idle costs. The serverless stack costs next to nothing when idle.

---

## 10. Future Improvements

Future plans for OpsBeacon AI include:
* **Multi-Channel Delivery**: Support webhooks for Slack, Microsoft Teams, and Discord.
* **Retrieval-Augmented Generation (RAG)**: Store previous summaries in a vector database (e.g. Pgvector or OpenSearch) to allow querying historical updates.
* **Agentic Collaboration**: Add a supervisor agent that can delegate deep-dive analysis of security patches to specialized code analysis subagents.

---

## 11. GitHub Repository

The source code for OpsBeacon AI is fully open-source and available on GitHub:
* **Repository Link**: [https://github.com/opsbeacon-ai/opsbeacon-ai](https://github.com/opsbeacon-ai/opsbeacon-ai)

The repository contains requirements, the SAM template, GitHub CI/CD configurations, unit tests, and comprehensive guides.

<!-- IMAGE_PLACEHOLDER: GitHub Repository -->
*Note: Capture a screenshot of the project repository on GitHub.*

---

## 12. Deployment

To deploy OpsBeacon AI to your own AWS account:

1. Request access to **Nova Lite** in the Bedrock console.
2. Verify your sender and recipient email addresses in the SES console.
3. Build and deploy using the AWS SAM CLI:
   ```bash
   sam build
   sam deploy --guided
   ```
4. Configure parameters (SenderEmail, RecipientEmail, BedrockModelId) as prompted.

For a full step-by-step setup guide, refer to the [Deployment Guide](file:///d:/AWS-weekend-challenge/docs/DEPLOYMENT.md) in the project docs.

---

## 13. Conclusion

OpsBeacon AI represents a complete, production-ready serverless agent that solves a real-world problem: staying up to date in the fast-moving DevOps space. By combining AWS Lambda, Amazon Bedrock, and Amazon SES, the agent operates autonomously, reliably, and cost-effectively.

This project shows how serverless architectures and generative AI models can automate routine knowledge gathering, allowing engineering teams to focus on building rather than searching for updates.
