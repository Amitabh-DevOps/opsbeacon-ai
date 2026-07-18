import unittest
from src.email_generator import generate_email_html, get_badge_class

class TestEmailGenerator(unittest.TestCase):
    def test_get_badge_class(self):
        """Test source name mapping to CSS class names."""
        self.assertEqual(get_badge_class("AWS What's New"), "badge-aws")
        self.assertEqual(get_badge_class("Kubernetes Blog"), "badge-k8s")
        self.assertEqual(get_badge_class("CNCF Blog"), "badge-cncf")
        self.assertEqual(get_badge_class("Docker Blog"), "badge-docker")
        self.assertEqual(get_badge_class("Unknown Source"), "badge-generic")

    def test_generate_email_html(self):
        """Test HTML rendering logic compiles data into the template."""
        mock_digest = {
            "updates": [
                {
                    "title": "Amazon Bedrock Nova Lite Release",
                    "source": "AWS What's New",
                    "url": "https://aws.amazon.com/whats-new/bedrock-nova",
                    "summary": "Nova Lite is ready to use.",
                    "why_it_matters": "Extremely cost efficient.",
                    "devops_impact": "Lower bills for summarizers."
                }
            ],
            "learning": {
                "interview_question": "Explain Bedrock Nova Lite architecture.",
                "hands_on_challenge": "Deploy a Lambda function calling Bedrock.",
                "recommendation": "Read AWS Nova Lite specs."
            }
        }

        html = generate_email_html(mock_digest)
        
        self.assertIsNotNone(html)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("Amazon Bedrock Nova Lite Release", html)
        self.assertIn("badge-aws", html)
        self.assertIn("Explain Bedrock Nova Lite architecture.", html)
        self.assertIn("Deploy a Lambda function calling Bedrock.", html)
        self.assertIn("Read AWS Nova Lite specs.", html)

    def test_generate_email_html_empty(self):
        """Test HTML rendering when there are no updates."""
        mock_digest = {
            "updates": [],
            "learning": {
                "interview_question": "Explain general CI/CD practices.",
                "hands_on_challenge": "Build a pipeline.",
                "recommendation": "Read CI/CD handbook."
            }
        }

        html = generate_email_html(mock_digest)
        self.assertIn("No major updates were released", html)
        self.assertIn("Explain general CI/CD practices.", html)
