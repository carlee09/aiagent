"""Temporal trend analysis for research data."""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from src.utils.logger import get_logger


class TrendAnalyzer:
    """Analyzes temporal trends in collected data."""

    def __init__(self):
        """Initialize trend analyzer."""
        self.logger = get_logger(self.__class__.__name__)

    def analyze_temporal_trends(
        self,
        data_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze temporal trends in data.

        Args:
            data_items: List of data items with dates

        Returns:
            Dictionary with temporal trend information
        """
        if not data_items:
            return self._empty_result()

        self.logger.info(f"Analyzing temporal trends for {len(data_items)} items")

        # Group items by date
        items_by_date = self._group_by_date(data_items)

        # Analyze X engagement trends if available
        engagement_trends = self._analyze_engagement_trends(data_items)

        # Get timeline summary
        timeline = self._get_timeline_summary(items_by_date)

        # Calculate posting frequency
        frequency = self._calculate_frequency(items_by_date)

        result = {
            "timeline": timeline,
            "frequency": frequency,
            "engagement_trends": engagement_trends,
            "total_dates": len(items_by_date),
            "date_range": self._get_date_range(items_by_date)
        }

        self.logger.info(f"Trend analysis complete: {len(items_by_date)} unique dates")
        return result

    def _group_by_date(
        self,
        data_items: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group data items by date.

        Args:
            data_items: List of data items

        Returns:
            Dictionary mapping date string to items
        """
        grouped = defaultdict(list)

        for item in data_items:
            date_str = item.get("date", "")
            if not date_str:
                # Try to parse from metadata
                date_str = item.get("metadata", {}).get("date", "Unknown")

            # Normalize date to just the date part (no time)
            try:
                if date_str and date_str != "Unknown":
                    # Try to parse various date formats
                    parsed_date = self._parse_date(date_str)
                    if parsed_date:
                        date_key = parsed_date.strftime("%Y-%m-%d")
                    else:
                        date_key = "Unknown"
                else:
                    date_key = "Unknown"
            except Exception:
                date_key = "Unknown"

            grouped[date_key].append(item)

        return dict(grouped)

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """
        Parse date string to datetime object.

        Args:
            date_str: Date string in various formats

        Returns:
            Datetime object or None if parsing fails
        """
        # Common date formats
        formats = [
            "%Y-%m-%d",
            "%Y-%m-%d %H:%M:%S",
            "%Y/%m/%d",
            "%d-%m-%Y",
            "%m/%d/%Y",
            "%B %d, %Y",
            "%b %d, %Y",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except (ValueError, TypeError):
                continue

        # Try ISO format
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            pass

        return None

    def _get_timeline_summary(
        self,
        items_by_date: Dict[str, List[Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        """
        Generate timeline summary.

        Args:
            items_by_date: Items grouped by date

        Returns:
            List of timeline entries
        """
        timeline = []

        # Sort dates
        sorted_dates = sorted([d for d in items_by_date.keys() if d != "Unknown"])

        for date in sorted_dates:
            items = items_by_date[date]
            count = len(items)

            # Calculate average engagement for this date
            total_engagement = 0
            engagement_count = 0

            for item in items:
                if item.get("source") == "x":
                    engagement = item.get("engagement", {})
                    likes = engagement.get("likes", 0)
                    retweets = engagement.get("retweets", 0)
                    total_engagement += likes + retweets
                    engagement_count += 1

            avg_engagement = total_engagement / engagement_count if engagement_count > 0 else 0

            timeline.append({
                "date": date,
                "count": count,
                "avg_engagement": round(avg_engagement, 1)
            })

        return timeline

    def _calculate_frequency(
        self,
        items_by_date: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        Calculate posting frequency statistics.

        Args:
            items_by_date: Items grouped by date

        Returns:
            Frequency statistics
        """
        dates = [d for d in items_by_date.keys() if d != "Unknown"]

        if not dates:
            return {
                "total_days": 0,
                "avg_per_day": 0.0,
                "max_per_day": 0,
                "min_per_day": 0
            }

        counts = [len(items_by_date[d]) for d in dates]

        return {
            "total_days": len(dates),
            "avg_per_day": round(sum(counts) / len(counts), 1) if counts else 0.0,
            "max_per_day": max(counts) if counts else 0,
            "min_per_day": min(counts) if counts else 0
        }

    def _analyze_engagement_trends(
        self,
        data_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze engagement trends for X posts.

        Args:
            data_items: List of data items

        Returns:
            Engagement trend statistics
        """
        x_items = [item for item in data_items if item.get("source") == "x"]

        if not x_items:
            return {
                "available": False,
                "total_posts": 0
            }

        total_likes = 0
        total_retweets = 0
        total_replies = 0

        for item in x_items:
            engagement = item.get("engagement", {})
            total_likes += engagement.get("likes", 0)
            total_retweets += engagement.get("retweets", 0)
            total_replies += engagement.get("replies", 0)

        count = len(x_items)

        return {
            "available": True,
            "total_posts": count,
            "avg_likes": round(total_likes / count, 1) if count > 0 else 0,
            "avg_retweets": round(total_retweets / count, 1) if count > 0 else 0,
            "avg_replies": round(total_replies / count, 1) if count > 0 else 0,
            "total_engagement": total_likes + total_retweets + total_replies
        }

    def _get_date_range(
        self,
        items_by_date: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, str]:
        """
        Get date range of data.

        Args:
            items_by_date: Items grouped by date

        Returns:
            Dictionary with start and end dates
        """
        dates = [d for d in items_by_date.keys() if d != "Unknown"]

        if not dates:
            return {"start": "Unknown", "end": "Unknown"}

        sorted_dates = sorted(dates)

        return {
            "start": sorted_dates[0],
            "end": sorted_dates[-1]
        }

    def _empty_result(self) -> Dict[str, Any]:
        """Return empty trend result."""
        return {
            "timeline": [],
            "frequency": {
                "total_days": 0,
                "avg_per_day": 0.0,
                "max_per_day": 0,
                "min_per_day": 0
            },
            "engagement_trends": {
                "available": False,
                "total_posts": 0
            },
            "total_dates": 0,
            "date_range": {"start": "Unknown", "end": "Unknown"}
        }
