import json
import re
import boto3  # type: ignore
from botocore.exceptions import ClientError  # type: ignore
from typing import Any
from src.logger import get_logger

logger = get_logger(__name__)


class BedrockClient:
    """
    Wrapper client for Amazon Bedrock using Nova Lite to summarize updates and generate learning materials.
    """

    def __init__(
        self, model_id: str = "amazon.nova-lite-v1:0", region_name: str = "us-east-1"
    ):
        """
        Initializes the BedrockClient.

        Args:
            model_id: The Amazon Bedrock Model ID to invoke.
            region_name: The AWS region where Bedrock is configured.
        """
        self.model_id = model_id
        self.client = boto3.client("bedrock-runtime", region_name=region_name)

    def generate_digest(self, feed_items: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Invokes Amazon Bedrock to process feed items, filter duplicates, and create a DevOps summary digest.

        Args:
            feed_items: A list of dict entries representing scraped RSS articles.

        Returns:
            A parsed dictionary with keys: 'updates' (list) and 'learning' (dict).
        """
        logger.info(
            "Preparing Bedrock prompt",
            extra={
                "extra_fields": {
                    "items_count": len(feed_items),
                    "model_id": self.model_id,
                }
            },
        )

        prompt = self._build_prompt(feed_items)

        try:
            logger.info("Invoking Bedrock Converse API")
            response = self.client.converse(
                modelId=self.model_id,
                messages=[{"role": "user", "content": [{"text": prompt}]}],
                inferenceConfig={
                    "maxTokens": 3000,
                    "temperature": 0.2,
                    "topP": 0.9,
                },
            )

            response_text = response["output"]["message"]["content"][0]["text"]
            logger.info("Bedrock API call successful, parsing response")
            return self._parse_json_response(response_text)

        except ClientError as exc:
            logger.error(
                "Bedrock ClientError during invocation",
                exc_info=True,
                extra={"extra_fields": {"error": str(exc)}},
            )
            return self._get_fallback_digest(
                f"AWS Bedrock Service Error occurred while generating the digest: {str(exc)}"
            )
        except Exception as exc:
            logger.error(
                "Unexpected error during Bedrock invocation",
                exc_info=True,
                extra={"extra_fields": {"error": str(exc)}},
            )
            return self._get_fallback_digest(
                f"An unexpected system error occurred while generating the digest: {str(exc)}"
            )

    def _build_prompt(self, feed_items: list[dict[str, Any]]) -> str:
        """
        Constructs the detailed prompt instructing Bedrock to output structured JSON content.
        """
        json_schema_format = """
{
  "updates": [
    {
      "title": "Clean, concise title of the update",
      "source": "AWS What's New / Kubernetes Blog / CNCF Blog / Docker Blog",
      "url": "URL link to the article",
      "summary": "2-3 sentence technical summary of what was released or announced.",
      "why_it_matters": "Explanation of the engineering value and relevance.",
      "devops_impact": "Direct operational impact on DevOps engineers (e.g., cost, complexity, pipeline changes)."
    }
  ],
  "learning": {
    "interview_question": "A scenario-based technical DevOps interview question related to these updates or cloud practices.",
    "hands_on_challenge": "A practical mini-challenge that a DevOps engineer can build in 30 minutes to learn this concept.",
    "recommendation": "A suggested topic, command, or tool to research further."
  }
}
"""

        if not feed_items:
            return f"""You are OpsBeacon, an expert DevOps AI intelligence assistant.
No recent cloud or DevOps updates were published in the last 24 hours.

Please output a valid JSON response following this structure:
{json_schema_format}

Since there are no feed items:
1. Keep the "updates" array empty.
2. In the "learning" section, generate a premium scenario-based DevOps interview question, a hands-on mini-challenge, and a learning recommendation that focuses on general advanced DevOps skills (e.g., IaC drift detection, container security hardening, or Kubernetes networking).

Response Requirements:
- You MUST respond ONLY with a valid JSON block.
- Do not output any chat prefix, suffix, or explanation.
- Wrap your JSON response in a markdown code block: ```json <json content> ```.
"""

        raw_items_str = json.dumps(feed_items, indent=2)

        return f"""You are OpsBeacon, an expert DevOps AI intelligence assistant.
Your task is to analyze, filter, and summarize the following cloud/DevOps updates.

Raw Feed Items:
{raw_items_str}

Please perform the following operations:
1. Deduplicate: If multiple feed articles describe the same announcement, merge them into a single update.
2. Filter: Discard general promotional content, marketing, or announcements that do not affect DevOps engineers, SREs, or cloud developers. Keep only technical updates.
3. Summarize & Extract: Generate summaries, explanations of why it matters, and concrete DevOps impacts.
4. Generate learning content: Generate a highly relevant DevOps interview question, hands-on challenge, and learning recommendation based directly on the updates.

You MUST format your output as a single, valid JSON block adhering to this schema:
{json_schema_format}

Response Requirements:
- You MUST respond ONLY with a valid JSON block.
- Do not output any chat prefix, suffix, or explanation.
- Wrap your JSON response in a markdown code block: ```json <json content> ```.
- Double-check that all JSON syntax is valid, strings are properly escaped, and JSON keys match exactly.
"""

    def _parse_json_response(self, text: str) -> dict[str, Any]:
        """
        Robustly extracts and parses JSON content from the LLM output.
        """
        # Look for markdown JSON block first
        match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
        json_str = match.group(1) if match else text

        try:
            parsed = json.loads(json_str.strip())

            # Simple schema validation
            if not isinstance(parsed, dict):
                raise ValueError("Parsed output is not a JSON object")
            if "updates" not in parsed:
                parsed["updates"] = []
            if "learning" not in parsed or not isinstance(parsed["learning"], dict):
                parsed["learning"] = {
                    "interview_question": "What is the best practice for managing secrets in Lambda?",
                    "hands_on_challenge": "Write a SAM template that injects secure parameters from Parameter Store.",
                    "recommendation": "Read the AWS Systems Manager Security best practices.",
                }
            return parsed

        except (json.JSONDecodeError, ValueError) as exc:
            logger.error(
                "Failed to parse Bedrock JSON output, using raw text fallback",
                extra={"extra_fields": {"error": str(exc), "raw_text": text}},
            )
            return self._get_fallback_digest(
                f"Failed to parse AI response. Raw output summary:\n\n{text[:1500]}"
            )

    def _get_fallback_digest(self, error_message: str) -> dict[str, Any]:
        """
        Returns a structured dictionary matching the schema when Bedrock fails or returns bad format.
        """
        return {
            "updates": [
                {
                    "title": "OpsBeacon Status Update",
                    "source": "OpsBeacon System",
                    "url": "https://github.com/opsbeacon-ai",
                    "summary": f"OpsBeacon AI executed successfully but encountered an issue compiling feed details: {error_message}",
                    "why_it_matters": "Ensures the system still sends daily heartbeat emails even when processing errors occur.",
                    "devops_impact": "None. Operational workflows are unaffected.",
                }
            ],
            "learning": {
                "interview_question": "How do you build a resilient notification system in AWS when downstream dependencies fail?",
                "hands_on_challenge": "Create an Amazon SES failure-handling architecture using Dead Letter Queues (DLQ).",
                "recommendation": "Examine the AWS Serverless Application Lens documentation for reliability patterns.",
            },
        }
