import os
from dataclasses import dataclass
from typing import Self

@dataclass(frozen=True)
class Config:
    """
    Configuration configuration class validating all required and optional env variables.
    """
    aws_region: str
    bedrock_model_id: str
    sender_email: str
    recipient_email: str
    rss_limit: int

    @classmethod
    def from_env(cls) -> Self:
        """
        Loads configuration from environment variables and validates presence.
        
        Raises:
            ValueError: If SENDER_EMAIL or RECIPIENT_EMAIL are missing, or RSS_LIMIT is not a valid int.
        """
        sender_email = os.environ.get("SENDER_EMAIL")
        recipient_email = os.environ.get("RECIPIENT_EMAIL")
        
        if not sender_email:
            raise ValueError("Missing required environment variable: SENDER_EMAIL")
        if not recipient_email:
            raise ValueError("Missing required environment variable: RECIPIENT_EMAIL")
            
        rss_limit_str = os.environ.get("RSS_LIMIT", "5")
        try:
            rss_limit = int(rss_limit_str)
        except ValueError as exc:
            raise ValueError(f"RSS_LIMIT must be an integer, got: {rss_limit_str}") from exc

        return cls(
            aws_region=os.environ.get("AWS_REGION", "us-east-1"),
            bedrock_model_id=os.environ.get("BEDROCK_MODEL_ID", "amazon.nova-lite-v1:0"),
            sender_email=sender_email,
            recipient_email=recipient_email,
            rss_limit=rss_limit,
        )
