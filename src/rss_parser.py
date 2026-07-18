from datetime import datetime, timezone, timedelta
import feedparser  # type: ignore
from typing import Any
from src.logger import get_logger

logger = get_logger(__name__)

DEFAULT_FEEDS = {
    "AWS What's New": "https://aws.amazon.com/about-aws/whats-new/recent/feed/",
    "Kubernetes Blog": "https://kubernetes.io/feed.xml",
    "CNCF Blog": "https://www.cncf.io/feed/",
    "Docker Blog": "https://www.docker.com/blog/feed/",
}


class RSSParser:
    """
    Client for fetching and parsing RSS feeds, filtering for items from the last 24 hours.
    """

    def __init__(self, limit: int = 5):
        """
        Initializes the RSSParser.

        Args:
            limit: Maximum items to extract per feed to prevent Bedrock prompt bloat.
        """
        self.limit = limit

    def fetch_recent_updates(
        self, feeds: dict[str, str] = DEFAULT_FEEDS
    ) -> list[dict[str, Any]]:
        """
        Fetches, parses, and aggregates recent updates from all configured feeds.

        Args:
            feeds: Dictionary mapping source names to feed URLs.

        Returns:
            A list of dictionary objects representing filtered articles.
        """
        now = datetime.now(timezone.utc)
        cutoff_time = now - timedelta(hours=24)
        aggregated_items: list[dict[str, Any]] = []

        logger.info(
            "Starting RSS feed collection",
            extra={
                "extra_fields": {
                    "feeds_count": len(feeds),
                    "cutoff_time": cutoff_time.isoformat(),
                }
            },
        )

        for source_name, feed_url in feeds.items():
            try:
                logger.info(
                    "Fetching feed",
                    extra={"extra_fields": {"source": source_name, "url": feed_url}},
                )
                parsed_feed = feedparser.parse(feed_url)

                # Check for feedparser specific parsing errors
                if hasattr(parsed_feed, "bozo") and parsed_feed.bozo:
                    exception_msg = str(parsed_feed.bozo_exception)
                    logger.warning(
                        "Feed parsing completed with warnings (bozo bit set)",
                        extra={
                            "extra_fields": {
                                "source": source_name,
                                "error": exception_msg,
                            }
                        },
                    )

                entries_processed = 0
                for entry in parsed_feed.entries:
                    if entries_processed >= self.limit:
                        logger.info(
                            "Reached RSS limit for feed",
                            extra={
                                "extra_fields": {
                                    "source": source_name,
                                    "limit": self.limit,
                                }
                            },
                        )
                        break

                    published_dt = self._parse_published_date(entry)
                    if not published_dt:
                        # Fallback: if no date is found, skip or default to now (let's skip for accuracy)
                        logger.warning(
                            "Could not determine published date for entry, skipping",
                            extra={
                                "extra_fields": {
                                    "source": source_name,
                                    "entry_title": entry.get("title", "Untitled"),
                                }
                            },
                        )
                        continue

                    # Filter for entries within the last 24 hours
                    if published_dt >= cutoff_time:
                        summary_content = entry.get(
                            "summary", entry.get("description", "")
                        )
                        # Clean up HTML tags from summary if needed, but feedparser generally returns a string.
                        # We will keep it simple and clean.
                        aggregated_items.append(
                            {
                                "title": entry.get("title", "Untitled").strip(),
                                "link": entry.get("link", "").strip(),
                                "published": published_dt.isoformat(),
                                "summary": summary_content.strip()[
                                    :1000
                                ],  # Truncate summary length to avoid prompt overflow
                                "source": source_name,
                            }
                        )
                        entries_processed += 1

                logger.info(
                    "Successfully processed feed",
                    extra={
                        "extra_fields": {
                            "source": source_name,
                            "items_found": entries_processed,
                        }
                    },
                )

            except Exception as exc:
                # Fail-safe: log exception and continue to next RSS feed
                logger.error(
                    "Failed to parse feed",
                    exc_info=True,
                    extra={
                        "extra_fields": {
                            "source": source_name,
                            "url": feed_url,
                            "error": str(exc),
                        }
                    },
                )

        logger.info(
            "RSS feed collection complete",
            extra={"extra_fields": {"total_items": len(aggregated_items)}},
        )
        return aggregated_items

    def _parse_published_date(self, entry: Any) -> datetime | None:
        """
        Safely extracts and converts publication date from a feed entry.

        Args:
            entry: The feedparser entry object.

        Returns:
            A timezone-aware UTC datetime object, or None if parsing fails.
        """
        # Try standard feedparser parsed date tuple first
        published_parsed = entry.get("published_parsed") or entry.get("updated_parsed")
        if published_parsed:
            try:
                # time.struct_time to datetime object in UTC
                return datetime(*published_parsed[:6], tzinfo=timezone.utc)
            except Exception:
                pass

        # Try parsing date strings manually if parsed representation is missing
        date_fields = ["published", "pubDate", "updated", "date"]
        for field in date_fields:
            date_str = entry.get(field)
            if date_str:
                for date_format in (
                    "%a, %d %b %Y %H:%M:%S %Z",  # RFC 822
                    "%Y-%m-%dT%H:%M:%S%z",  # ISO 8601
                    "%Y-%m-%dT%H:%M:%SZ",  # ISO 8601 UTC
                    "%Y-%m-%d %H:%M:%S",
                ):
                    try:
                        dt = datetime.strptime(date_str, date_format)
                        if dt.tzinfo is None:
                            dt = dt.replace(tzinfo=timezone.utc)
                        return dt.astimezone(timezone.utc)
                    except ValueError:
                        continue
        return None
