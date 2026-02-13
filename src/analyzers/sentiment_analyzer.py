"""Sentiment analysis for research data."""

from typing import Dict, List, Any
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from src.utils.logger import get_logger


class SentimentAnalyzer:
    """Analyzes sentiment of collected data using VADER."""

    def __init__(self):
        """Initialize sentiment analyzer."""
        self.analyzer = SentimentIntensityAnalyzer()
        self.logger = get_logger(self.__class__.__name__)

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of a single text.

        Args:
            text: Text to analyze

        Returns:
            Dictionary with pos, neg, neu, compound scores
        """
        if not text or not text.strip():
            return {"pos": 0.0, "neg": 0.0, "neu": 1.0, "compound": 0.0}

        try:
            scores = self.analyzer.polarity_scores(text)
            return scores
        except Exception as e:
            self.logger.warning(f"Error analyzing sentiment: {e}")
            return {"pos": 0.0, "neg": 0.0, "neu": 1.0, "compound": 0.0}

    def analyze_items(self, data_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze sentiment across all data items.

        Args:
            data_items: List of data items to analyze

        Returns:
            Dictionary with overall sentiment statistics
        """
        if not data_items:
            return self._empty_result()

        self.logger.info(f"Analyzing sentiment for {len(data_items)} items")

        sentiments = []
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        total_compound = 0.0

        for item in data_items:
            # Analyze content field
            content = item.get("content", "") or item.get("title", "")
            if not content:
                continue

            sentiment = self.analyze_sentiment(content)
            sentiments.append(sentiment)

            # Categorize based on compound score
            compound = sentiment["compound"]
            total_compound += compound

            if compound >= 0.05:
                positive_count += 1
            elif compound <= -0.05:
                negative_count += 1
            else:
                neutral_count += 1

        if not sentiments:
            return self._empty_result()

        total = len(sentiments)
        avg_compound = total_compound / total if total > 0 else 0.0

        # Calculate percentages
        positive_pct = (positive_count / total * 100) if total > 0 else 0
        negative_pct = (negative_count / total * 100) if total > 0 else 0
        neutral_pct = (neutral_count / total * 100) if total > 0 else 0

        # Determine overall sentiment
        if avg_compound >= 0.05:
            overall = "Positive"
        elif avg_compound <= -0.05:
            overall = "Negative"
        else:
            overall = "Neutral"

        result = {
            "overall": overall,
            "average_compound": round(avg_compound, 3),
            "distribution": {
                "positive": {
                    "count": positive_count,
                    "percentage": round(positive_pct, 1)
                },
                "neutral": {
                    "count": neutral_count,
                    "percentage": round(neutral_pct, 1)
                },
                "negative": {
                    "count": negative_count,
                    "percentage": round(negative_pct, 1)
                }
            },
            "total_analyzed": total
        }

        self.logger.info(f"Sentiment analysis complete: {overall} (compound: {avg_compound:.3f})")
        return result

    def _empty_result(self) -> Dict[str, Any]:
        """Return empty sentiment result."""
        return {
            "overall": "Unknown",
            "average_compound": 0.0,
            "distribution": {
                "positive": {"count": 0, "percentage": 0.0},
                "neutral": {"count": 0, "percentage": 0.0},
                "negative": {"count": 0, "percentage": 0.0}
            },
            "total_analyzed": 0
        }

    def get_sentiment_label(self, compound: float) -> str:
        """
        Get sentiment label from compound score.

        Args:
            compound: Compound sentiment score

        Returns:
            Sentiment label string
        """
        if compound >= 0.05:
            return "Positive"
        elif compound <= -0.05:
            return "Negative"
        else:
            return "Neutral"
