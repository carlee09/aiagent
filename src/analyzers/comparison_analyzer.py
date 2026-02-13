"""Comparison analyzer for research reports."""

from typing import Dict, List, Any
from src.utils.logger import get_logger


class ComparisonAnalyzer:
    """Analyzes differences between current and previous research reports."""

    def __init__(self):
        """Initialize comparison analyzer."""
        self.logger = get_logger(self.__class__.__name__)

    def compare_analyses(
        self,
        current: Dict[str, Any],
        previous: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Compare current analysis with previous report.

        Args:
            current: Current analysis results
            previous: Previous report data

        Returns:
            Dictionary with comparison results
        """
        self.logger.info("Comparing current analysis with previous report")

        comparison = {}

        # Compare sentiment
        sentiment_comparison = self._compare_sentiment(
            current.get("sentiment"),
            previous.get("sentiment")
        )
        if sentiment_comparison:
            comparison["sentiment_change"] = sentiment_comparison

        # Compare keywords
        keyword_comparison = self._compare_keywords(
            current.get("keywords", []),
            previous.get("keywords", [])
        )
        if keyword_comparison:
            comparison.update(keyword_comparison)

        # Determine overall trend direction
        trend_direction = self._determine_trend_direction(
            sentiment_comparison,
            keyword_comparison
        )
        if trend_direction:
            comparison["trend_direction"] = trend_direction

        self.logger.info("Comparison analysis complete")
        return comparison

    def _compare_sentiment(
        self,
        current: Dict[str, Any],
        previous: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Compare sentiment between current and previous.

        Args:
            current: Current sentiment data
            previous: Previous sentiment data

        Returns:
            Sentiment comparison data
        """
        if not current or not previous:
            return None

        current_overall = current.get("overall", "Unknown")
        previous_overall = previous.get("overall", "Unknown")

        if current_overall == previous_overall:
            direction = "→"  # No change
        elif current_overall == "Positive" and previous_overall != "Positive":
            direction = "↗️"  # Improved
        elif current_overall == "Negative" and previous_overall != "Negative":
            direction = "↘️"  # Declined
        else:
            direction = "↔️"  # Mixed

        current_compound = current.get("average_compound", 0.0)
        previous_compound = previous.get("average_compound", 0.0)
        compound_change = current_compound - previous_compound

        return {
            "old": previous_overall,
            "new": current_overall,
            "direction": direction,
            "compound_change": round(compound_change, 3)
        }

    def _compare_keywords(
        self,
        current_keywords: List,
        previous_keywords: List[str]
    ) -> Dict[str, List[str]]:
        """
        Compare keywords between current and previous.

        Args:
            current_keywords: Current keywords (list of tuples)
            previous_keywords: Previous keywords (list of strings)

        Returns:
            Keyword comparison data
        """
        if not current_keywords:
            return {}

        # Extract just the keyword strings from current (may be tuples)
        if current_keywords and isinstance(current_keywords[0], tuple):
            current_kw_list = [kw[0] for kw in current_keywords]
        else:
            current_kw_list = current_keywords

        if not previous_keywords:
            # All keywords are new
            return {
                "new_topics": current_kw_list[:10],
                "removed_topics": []
            }

        # Normalize keywords (lowercase for comparison)
        current_set = set(kw.lower() for kw in current_kw_list)
        previous_set = set(kw.lower() for kw in previous_keywords)

        # Find new and removed topics
        new_topics = list(current_set - previous_set)
        removed_topics = list(previous_set - current_set)

        # Map back to original case for display
        new_topics_display = [
            kw for kw in current_kw_list if kw.lower() in new_topics
        ][:10]

        removed_topics_display = [
            kw for kw in previous_keywords if kw.lower() in removed_topics
        ][:10]

        return {
            "new_topics": new_topics_display,
            "removed_topics": removed_topics_display,
            "total_new": len(new_topics),
            "total_removed": len(removed_topics)
        }

    def _determine_trend_direction(
        self,
        sentiment_comparison: Dict[str, str],
        keyword_comparison: Dict[str, List[str]]
    ) -> str:
        """
        Determine overall trend direction.

        Args:
            sentiment_comparison: Sentiment comparison data
            keyword_comparison: Keyword comparison data

        Returns:
            Trend direction description
        """
        if not sentiment_comparison and not keyword_comparison:
            return ""

        trends = []

        # Sentiment trend
        if sentiment_comparison:
            direction = sentiment_comparison.get("direction", "")
            if direction == "↗️":
                trends.append("Sentiment improving")
            elif direction == "↘️":
                trends.append("Sentiment declining")
            elif direction == "→":
                trends.append("Sentiment stable")

        # Topic evolution trend
        if keyword_comparison:
            new_count = keyword_comparison.get("total_new", 0)
            removed_count = keyword_comparison.get("total_removed", 0)

            if new_count > removed_count * 1.5:
                trends.append("Many new topics emerging")
            elif removed_count > new_count * 1.5:
                trends.append("Focus narrowing")
            else:
                trends.append("Topic evolution balanced")

        return " | ".join(trends) if trends else "Stable"

    def identify_changes(
        self,
        current_data: List[Dict[str, Any]],
        previous_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Identify specific changes between data sets.

        Args:
            current_data: Current data items
            previous_data: Previous data items

        Returns:
            Dictionary with identified changes
        """
        # This method is for future enhancement to compare actual data items
        # Currently not used in the main workflow
        return {
            "current_count": len(current_data),
            "previous_count": len(previous_data),
            "change": len(current_data) - len(previous_data)
        }

    def calculate_trend_direction(
        self,
        metric_old: float,
        metric_new: float
    ) -> str:
        """
        Calculate trend direction for a metric.

        Args:
            metric_old: Old metric value
            metric_new: New metric value

        Returns:
            Trend direction string
        """
        if metric_new > metric_old * 1.1:
            return "↗️ Increasing"
        elif metric_new < metric_old * 0.9:
            return "↘️ Decreasing"
        else:
            return "→ Stable"
