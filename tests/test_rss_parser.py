import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone, timedelta
from src.rss_parser import RSSParser


class TestRSSParser(unittest.TestCase):
    def setUp(self):
        self.parser = RSSParser(limit=5)

    def test_parse_published_date_struct(self):
        """Test parsing when published_parsed is a struct_time."""
        entry = MagicMock()
        entry.get.side_effect = lambda key, default=None: {
            "published_parsed": (2026, 7, 18, 12, 0, 0, 5, 200, 0)
        }.get(key, default)

        dt = self.parser._parse_published_date(entry)
        self.assertIsNotNone(dt)
        self.assertEqual(dt, datetime(2026, 7, 18, 12, 0, 0, tzinfo=timezone.utc))

    def test_parse_published_date_string(self):
        """Test parsing when date is a string (RFC 822 / ISO 8601)."""
        entry = MagicMock()
        # Mock pubDate string
        entry.get.side_effect = lambda key, default=None: {
            "pubDate": "Sat, 18 Jul 2026 12:00:00 GMT"
        }.get(key, default)

        dt = self.parser._parse_published_date(entry)
        self.assertIsNotNone(dt)
        self.assertEqual(dt.year, 2026)
        self.assertEqual(dt.month, 7)
        self.assertEqual(dt.day, 18)

    @patch("feedparser.parse")
    def test_fetch_recent_updates_filtering(self, mock_parse):
        """Test that updates older than 24 hours are filtered out."""
        now = datetime.now(timezone.utc)
        recent_time = now - timedelta(hours=3)
        old_time = now - timedelta(hours=28)

        # Convert to struct_time for published_parsed mock
        recent_struct = recent_time.timetuple()
        old_struct = old_time.timetuple()

        mock_feed = MagicMock()
        mock_entry_recent = MagicMock()
        mock_entry_recent.get.side_effect = lambda key, default=None: {
            "title": "Recent Kubernetes release",
            "link": "https://k8s.io/new",
            "published_parsed": recent_struct,
            "summary": "Kubernetes gets updates.",
        }.get(key, default)

        mock_entry_old = MagicMock()
        mock_entry_old.get.side_effect = lambda key, default=None: {
            "title": "Old Docker release",
            "link": "https://docker.com/old",
            "published_parsed": old_struct,
            "summary": "Docker has updates.",
        }.get(key, default)

        mock_feed.entries = [mock_entry_recent, mock_entry_old]
        mock_parse.return_value = mock_feed

        updates = self.parser.fetch_recent_updates(
            {"Kubernetes Blog": "http://test.com"}
        )

        self.assertEqual(len(updates), 1)
        self.assertEqual(updates[0]["title"], "Recent Kubernetes release")
        self.assertEqual(updates[0]["source"], "Kubernetes Blog")

    @patch("feedparser.parse")
    def test_fetch_recent_updates_failure(self, mock_parse):
        """Test that feed errors are handled gracefully and do not crash the app."""
        mock_parse.side_effect = Exception("Connection timed out")

        # Should not raise exception
        updates = self.parser.fetch_recent_updates(
            {"AWS What's New": "http://aws-feed.com"}
        )
        self.assertEqual(updates, [])
