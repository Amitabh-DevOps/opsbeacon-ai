import unittest
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError  # type: ignore
from src.ses_client import SESClient


class TestSESClient(unittest.TestCase):
    @patch("boto3.client")
    def test_send_email_success(self, mock_boto):
        """Test that send_email returns True when AWS SES succeeds."""
        mock_ses = MagicMock()
        mock_boto.return_value = mock_ses
        mock_ses.send_email.return_value = {"MessageId": "msg-12345"}

        client = SESClient()
        success = client.send_email(
            sender="sender@example.com",
            recipient="recipient@example.com",
            subject="Test Subject",
            html_body="<h1>Hello</h1>",
        )

        self.assertTrue(success)
        mock_ses.send_email.assert_called_once()

    @patch("boto3.client")
    def test_send_email_client_error(self, mock_boto):
        """Test that ClientError is caught and returns False."""
        mock_ses = MagicMock()
        mock_boto.return_value = mock_ses
        mock_ses.send_email.side_effect = ClientError(
            {
                "Error": {
                    "Code": "MessageRejected",
                    "Message": "Email address is not verified",
                }
            },
            "SendEmail",
        )

        client = SESClient()
        success = client.send_email(
            sender="sender@example.com",
            recipient="recipient@example.com",
            subject="Test Subject",
            html_body="<h1>Hello</h1>",
        )

        self.assertFalse(success)

    @patch("boto3.client")
    def test_send_email_generic_exception(self, mock_boto):
        """Test that general exceptions are caught and return False."""
        mock_ses = MagicMock()
        mock_boto.return_value = mock_ses
        mock_ses.send_email.side_effect = Exception("Network Connection Lost")

        client = SESClient()
        success = client.send_email(
            sender="sender@example.com",
            recipient="recipient@example.com",
            subject="Test Subject",
            html_body="<h1>Hello</h1>",
        )

        self.assertFalse(success)
