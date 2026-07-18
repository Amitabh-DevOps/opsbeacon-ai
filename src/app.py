from typing import Any
from src.logger import get_logger
from src.config import Config
from src.rss_parser import RSSParser
from src.bedrock_client import BedrockClient
from src.email_generator import generate_email_html
from src.ses_client import SESClient

logger = get_logger(__name__)

def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """
    AWS Lambda handler function triggered by EventBridge Scheduler.
    Runs the full OpsBeacon AI agent workflow: fetching, summarizing, and emailing updates.
    
    Args:
        event: AWS Lambda Event dict.
        context: AWS Lambda Context object.
        
    Returns:
        A dictionary response indicating completion status.
    """
    logger.info("OpsBeacon AI agent workflow execution started", extra={"extra_fields": {"event": event}})

    try:
        # 1. Load and validate configuration
        logger.info("Initializing configuration parameters")
        config = Config.from_env()

        # 2. Gather RSS Updates from last 24 hours
        logger.info("Retrieving RSS feeds")
        parser = RSSParser(limit=config.rss_limit)
        updates = parser.fetch_recent_updates()

        # 3. Analyze and summarize updates using Amazon Bedrock Nova Lite
        logger.info("Processing updates with Amazon Bedrock")
        bedrock = BedrockClient(model_id=config.bedrock_model_id, region_name=config.aws_region)
        digest = bedrock.generate_digest(updates)

        # 4. Generate structured HTML email newsletter
        logger.info("Compiling daily briefing newsletter HTML")
        html_body = generate_email_html(digest)

        # 5. Send daily briefing via Amazon SES
        logger.info("Dispatching daily briefing email")
        ses = SESClient(region_name=config.aws_region)
        
        # Prepare subject line with dynamic date
        now_date = digest.get("date")
        if not now_date:
            import datetime
            now_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
            
        subject = f"OpsBeacon AI: Daily DevOps Intelligence Briefing ({now_date})"
        
        email_sent = ses.send_email(
            sender=config.sender_email,
            recipient=config.recipient_email,
            subject=subject,
            html_body=html_body
        )

        if email_sent:
            logger.info("OpsBeacon AI workflow completed successfully")
            return {
                "statusCode": 200,
                "body": "OpsBeacon AI daily briefing compiled and sent successfully."
            }
        else:
            logger.error("OpsBeacon AI workflow failed to send email")
            return {
                "statusCode": 500,
                "body": "Failed to send the OpsBeacon AI daily email. Check CloudWatch logs for details."
            }

    except Exception as exc:
        logger.error("Fatal exception during OpsBeacon AI execution", exc_info=True, extra={"extra_fields": {"error": str(exc)}})
        return {
            "statusCode": 500,
            "body": f"Fatal exception during OpsBeacon AI agent run: {str(exc)}"
        }

if __name__ == "__main__":
    # Local execution helper
    import sys
    import os
    logger.info("Running locally for debugging")
    # Setup some test mock variables if missing
    os.environ.setdefault("SENDER_EMAIL", "sender@example.com")
    os.environ.setdefault("RECIPIENT_EMAIL", "recipient@example.com")
    os.environ.setdefault("BEDROCK_MODEL_ID", "amazon.nova-lite-v1:0")
    os.environ.setdefault("AWS_REGION", "us-east-1")
    lambda_handler({}, None)
