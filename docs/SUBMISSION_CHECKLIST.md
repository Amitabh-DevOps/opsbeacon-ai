# AWS Builder Center - Submission Checklist

This checklist verifies that **OpsBeacon AI** meets all the requirements specified for the **Build an Always-On Agent Weekend Challenge**.

---

## Challenge Requirements Check

* [x] **AI-Powered**: Integrates with Amazon Bedrock Nova Lite to deduplicate feeds, summarize text, and generate custom learning challenges and interview questions.
* [x] **Runs Unattended**: Executes completely autonomously without any user trigger or clicking.
* [x] **Triggered Automatically**: Uses EventBridge Scheduler with a daily cron schedule (`cron(0 8 * * ? *)`).
* [x] **Does Useful Work**: Scrapes cloud/DevOps RSS blogs, filters for updates from the last 24 hours, aggregates technical context, and generates learning items.
* [x] **Reports Results**: Delivers a beautiful, responsive HTML email briefing directly to the user's inbox via Amazon SES.
* [x] **Uses AWS Services**: EventBridge Scheduler, AWS Lambda, Amazon Bedrock, Amazon SES, and CloudWatch.
* [x] **AWS Free Tier Friendly**: Fits entirely within the AWS Free Tier, costing less than $0.02/month.
* [x] **Evidence of Unattended Execution**: Detailed structured JSON logs are emitted to CloudWatch, capturing feed scrapes, LLM reasoning, and email success responses.
* [x] **Public GitHub Repository**: Complete repository structure ready to be pushed to GitHub with open-source LICENSE, Contributing guidelines, and Code of Conduct.
* [x] **Complete Documentation**:
  * `README.md` (detailed overview and guides)
  * `DEPLOYMENT.md` (step-by-step AWS provisioning)
  * `LOCAL_SETUP.md` (developer environment setup)
  * `TROUBLESHOOTING.md` (diagnostic guide for sandbox, Bedrock access, etc.)
  * `COST.md` (detailed Free Tier calculations)
  * `ROADMAP.md` (future architecture and integrations)
  * `demo-script.md` (2-minute video presentation guide)

---

## Article Specific Requirements Check

* [x] **Article Title**: Starts with `"Weekend Agent Challenge: OpsBeacon AI"` exactly.
* [x] **Article Tag**: Includes the required tag `agents`.
* [x] **Article Word Count**: Over 500 words (the generated article contains ~1100 words).
* [x] **Article Structure**: Covers all 13 sections required by the challenge.
* [x] **Architecture Diagrams**: Included in Mermaid and SVG format.
* [x] **Screenshot Placeholders**: Included in README, article, deployment, and troubleshooting guides with instructions.
