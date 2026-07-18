import unittest
from unittest.mock import patch, MagicMock
from src.app import lambda_handler

class TestAppLambda(unittest.TestCase):
    @patch("src.app.Config")
    @patch("src.app.RSSParser")
    @patch("src.app.BedrockClient")
    @patch("src.app.SESClient")
    def test_lambda_handler_success(self, mock_ses, mock_bedrock, mock_rss, mock_config):
        """Test successful execution path of lambda_handler."""
        # Mock Config
        mock_config_instance = MagicMock()
        mock_config_instance.rss_limit = 5
        mock_config_instance.aws_region = "us-east-1"
        mock_config_instance.bedrock_model_id = "amazon.nova-lite-v1:0"
        mock_config_instance.sender_email = "sender@example.com"
        mock_config_instance.recipient_email = "recipient@example.com"
        mock_config.from_env.return_value = mock_config_instance

        # Mock RSSParser
        mock_rss_instance = MagicMock()
        mock_rss_instance.fetch_recent_updates.return_value = [{"title": "AWS Lambda Node 22"}]
        mock_rss.return_value = mock_rss_instance

        # Mock BedrockClient
        mock_bedrock_instance = MagicMock()
        mock_bedrock_instance.generate_digest.return_value = {
            "date": "2026-07-18",
            "updates": [{"title": "AWS Lambda Node 22", "source": "AWS What's New", "url": "https://aws.com", "summary": "...", "why_it_matters": "...", "devops_impact": "..."}],
            "learning": {"interview_question": "...", "hands_on_challenge": "...", "recommendation": "..."}
        }
        mock_bedrock.return_value = mock_bedrock_instance

        # Mock SESClient
        mock_ses_instance = MagicMock()
        mock_ses_instance.send_email.return_value = True
        mock_ses.return_value = mock_ses_instance

        # Invoke handler
        response = lambda_handler({}, None)

        self.assertEqual(response["statusCode"], 200)
        self.assertIn("compiled and sent successfully", response["body"])
        
        mock_rss_instance.fetch_recent_updates.assert_called_once()
        mock_bedrock_instance.generate_digest.assert_called_once()
        mock_ses_instance.send_email.assert_called_once()

    @patch("src.app.Config")
    def test_lambda_handler_config_failure(self, mock_config):
        """Test that configuration failure is caught and returns 500."""
        mock_config.from_env.side_effect = ValueError("Missing configuration")

        response = lambda_handler({}, None)

        self.assertEqual(response["statusCode"], 500)
        self.assertIn("Fatal exception during OpsBeacon AI", response["body"])
