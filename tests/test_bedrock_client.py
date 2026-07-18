import unittest
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError  # type: ignore
from src.bedrock_client import BedrockClient


class TestBedrockClient(unittest.TestCase):
    @patch("boto3.client")
    def test_generate_digest_success(self, mock_boto):
        """Test successful bedrock call and JSON parser parsing."""
        mock_runtime = MagicMock()
        mock_boto.return_value = mock_runtime

        mock_response = {"output": {"message": {"content": [{"text": """
```json
{
  "updates": [
    {
      "title": "Amazon Bedrock Nova Available",
      "source": "AWS What's New",
      "url": "https://aws.amazon.com/whats-new/bedrock",
      "summary": "Amazon Bedrock Nova models are now generally available.",
      "why_it_matters": "Lowers inference cost significantly.",
      "devops_impact": "DevOps teams can migrate their automation scripts to Nova."
    }
  ],
  "learning": {
    "interview_question": "What are the advantages of Amazon Bedrock Nova Lite over Claude?",
    "hands_on_challenge": "Deploy an application that utilizes Nova Lite via Bedrock Converse API.",
    "recommendation": "Review the pricing details of Nova Lite."
  }
}
```
"""}]}}}
        mock_runtime.converse.return_value = mock_response

        client = BedrockClient()
        digest = client.generate_digest([{"title": "Some Update"}])

        self.assertEqual(len(digest["updates"]), 1)
        self.assertEqual(digest["updates"][0]["title"], "Amazon Bedrock Nova Available")
        self.assertEqual(
            digest["learning"]["interview_question"],
            "What are the advantages of Amazon Bedrock Nova Lite over Claude?",
        )

    @patch("boto3.client")
    def test_generate_digest_client_error(self, mock_boto):
        """Test fallback digest is returned on AWS API client error."""
        mock_runtime = MagicMock()
        mock_boto.return_value = mock_runtime

        # Simulate botocore ClientError
        mock_runtime.converse.side_effect = ClientError(
            {"Error": {"Code": "AccessDeniedException", "Message": "Access Denied"}},
            "Converse",
        )

        client = BedrockClient()
        digest = client.generate_digest([])

        self.assertEqual(len(digest["updates"]), 1)
        self.assertEqual(digest["updates"][0]["title"], "OpsBeacon Status Update")
        self.assertIn("Access Denied", digest["updates"][0]["summary"])

    def test_parse_json_response_raw_fallback(self):
        """Test that if LLM returns bad JSON, fallback handles it and returns fallback schema."""
        client = BedrockClient()
        # Bad JSON input
        bad_response = "Here is your response:\n{malformed_json_here"

        digest = client._parse_json_response(bad_response)
        self.assertEqual(digest["updates"][0]["title"], "OpsBeacon Status Update")
        self.assertIn("Failed to parse AI response", digest["updates"][0]["summary"])
