import boto3  # type: ignore
from botocore.exceptions import ClientError  # type: ignore
from src.logger import get_logger

logger = get_logger(__name__)


class SESClient:
    """
    Wrapper client for Amazon SES to handle email transmissions.
    """

    def __init__(self, region_name: str = "us-east-1"):
        """
        Initializes the SESClient.

        Args:
            region_name: The AWS region where SES is configured.
        """
        self.client = boto3.client("ses", region_name=region_name)

    def send_email(
        self, sender: str, recipient: str, subject: str, html_body: str
    ) -> bool:
        """
        Sends an HTML format email using verified SES identities.

        Args:
            sender: The verified source email address.
            recipient: The verified destination email address.
            subject: Email subject header.
            html_body: Email body in HTML format.

        Returns:
            True if transmission succeeds, False otherwise.
        """
        logger.info(
            "Initiating SES send_email",
            extra={
                "extra_fields": {
                    "sender": sender,
                    "recipient": recipient,
                    "subject": subject,
                }
            },
        )

        try:
            response = self.client.send_email(
                Source=sender,
                Destination={"ToAddresses": [recipient]},
                Message={
                    "Subject": {"Data": subject, "Charset": "UTF-8"},
                    "Body": {"Html": {"Data": html_body, "Charset": "UTF-8"}},
                },
            )

            message_id = response.get("MessageId", "N/A")
            logger.info(
                "Email dispatched successfully",
                extra={"extra_fields": {"message_id": message_id}},
            )
            return True

        except ClientError as exc:
            error_code = exc.response.get("Error", {}).get("Code", "Unknown")
            error_msg = exc.response.get("Error", {}).get("Message", "")

            logger.error(
                "SES ClientError sending email",
                exc_info=True,
                extra={
                    "extra_fields": {
                        "error_code": error_code,
                        "error_message": error_msg,
                        "sender": sender,
                        "recipient": recipient,
                    }
                },
            )

            # Specific troubleshooting advice printed to log for sandbox issues
            if (
                error_code == "MessageRejected"
                and "Email address is not verified" in error_msg
            ):
                logger.warning(
                    "SES verification failure: Make sure both sender and recipient addresses are fully verified in the SES Console."
                )
            elif error_code == "ProductionAccessNotGranted":
                logger.warning(
                    "SES sandbox restriction: Production access is not granted, ensure you are sending to verified email addresses only."
                )

            return False

        except Exception as exc:
            logger.error(
                "Unexpected error sending email through SES",
                exc_info=True,
                extra={"extra_fields": {"error": str(exc)}},
            )
            return False
