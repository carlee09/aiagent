"""Markdown report generator."""

from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

from src.config import Config
from src.utils.logger import get_logger


class MarkdownGenerator:
    """Generator for Markdown research reports."""

    def __init__(self):
        """Initialize Markdown generator."""
        self.logger = get_logger(self.__class__.__name__)

    def generate_report(
        self,
        topic: str,
        analysis_result: Dict[str, Any],
        sources: Dict[str, List[Dict[str, str]]],
        output_path: Path,
        sentiment: Dict[str, Any] = None,
        keywords: List[tuple] = None,
        trends: Dict[str, Any] = None,
        comparison: Dict[str, Any] = None
    ) -> bool:
        """
        Generate a comprehensive Markdown research report.

        Args:
            topic: Research topic
            analysis_result: Analysis results from Claude
            sources: Organized data sources
            output_path: Path to save the report

        Returns:
            True if successful, False otherwise
        """
        self.logger.info("📝 Generating Markdown report...")

        try:
            # Build report content
            report_content = self._build_report(
                topic, analysis_result, sources,
                sentiment, keywords, trends, comparison
            )

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to file
            output_path.write_text(report_content, encoding="utf-8")

            self.logger.info(f"✅ Report saved to: {output_path}")
            return True

        except Exception as e:
            self.logger.error(f"❌ Error generating report: {e}")
            return False

    def _build_report(
        self,
        topic: str,
        analysis_result: Dict[str, Any],
        sources: Dict[str, List[Dict[str, str]]],
        sentiment: Dict[str, Any] = None,
        keywords: List[tuple] = None,
        trends: Dict[str, Any] = None,
        comparison: Dict[str, Any] = None
    ) -> str:
        """
        Build the complete report content.

        Args:
            topic: Research topic
            analysis_result: Analysis results
            sources: Organized sources
            sentiment: Sentiment analysis results
            keywords: Keyword extraction results
            trends: Temporal trend analysis results
            comparison: Comparison with previous report

        Returns:
            Complete report content as string
        """
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        # Count sources
        x_count = len(sources.get("x", []))
        web_count = len(sources.get("web", []))
        total_sources = x_count + web_count

        # Get metadata
        metadata = analysis_result.get("metadata", {})
        model = metadata.get("model", "Claude Sonnet 4")
        tokens_used = metadata.get("tokens_used", "N/A")

        # Build report sections
        sections = []

        # Header
        sections.append(f"# {topic} - Research Report\n")
        sections.append(f"**Generated**: {timestamp}  ")
        sections.append(f"**Data Sources**: X ({x_count}), Web ({web_count}) - Total: {total_sources}  ")
        sections.append(f"**Analysis Model**: {model}  ")
        sections.append(f"**Tokens Used**: {tokens_used}  ")
        sections.append("\n---\n")

        # Quick Stats Dashboard (if enhanced features available)
        if sentiment or keywords or trends:
            sections.append(self._build_quick_stats(sentiment, keywords, trends))

        # Comparison section (if available)
        if comparison:
            sections.append(self._build_comparison_section(comparison))

        # Sentiment Analysis section
        if sentiment:
            sections.append(self._build_sentiment_section(sentiment))

        # Top Keywords section
        if keywords:
            sections.append(self._build_keywords_section(keywords))

        # Temporal Trends section
        if trends:
            sections.append(self._build_trends_section(trends))

        # Analysis content from Claude
        analysis_text = analysis_result.get("analysis", "")
        if analysis_text:
            sections.append(analysis_text)
            sections.append("\n---\n")

        # Data sources section
        sections.append("\n## 📚 Data Sources\n")

        # X sources
        if x_count > 0:
            sections.append(f"\n### X (Twitter) - {x_count} posts\n")
            for i, item in enumerate(sources["x"], 1):
                author = item.get("author", "Unknown")
                content = item.get("content", "")
                date = item.get("date", "")
                url = item.get("url", "")
                engagement = item.get("engagement", {})
                likes = engagement.get("likes", 0)

                # Display "N/A" if likes data is not available (0 or None)
                likes_display = "N/A" if likes == 0 else f"{likes}"

                sections.append(f"{i}. **@{author}** - {date}  ")
                sections.append(f"   {content}  ")
                sections.append(f"   👍 {likes_display} likes | [View Tweet]({url})  \n")

        # Web sources
        if web_count > 0:
            sections.append(f"\n### Web - {web_count} results\n")
            for i, item in enumerate(sources["web"], 1):
                title = item.get("title", "Untitled")
                source = item.get("source", "Unknown")
                date = item.get("date", "")
                url = item.get("url", "")

                sections.append(f"{i}. **{title}**  ")
                sections.append(f"   Source: {source} | Date: {date}  ")
                sections.append(f"   [Read Article]({url})  \n")

        # Footer
        sections.append("\n---\n")
        sections.append("\n*This report was generated by Research Agent - AI-powered research automation tool*\n")

        return "\n".join(sections)

    def generate_filename(self, topic: str) -> str:
        """
        Generate a filename for the report.

        Args:
            topic: Research topic

        Returns:
            Filename string
        """
        # Sanitize topic for filename
        safe_topic = "".join(c if c.isalnum() or c in (" ", "-", "_") else "" for c in topic)
        safe_topic = safe_topic.strip().replace(" ", "-")[:50]  # Limit length

        # Add timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        return f"research_{safe_topic}_{timestamp}.md"

    def _build_quick_stats(
        self,
        sentiment: Dict[str, Any],
        keywords: List[tuple],
        trends: Dict[str, Any]
    ) -> str:
        """Build quick stats dashboard section."""
        sections = []
        sections.append("\n## 📊 Quick Stats\n")

        stats = []

        if sentiment:
            overall = sentiment.get("overall", "Unknown")
            compound = sentiment.get("average_compound", 0.0)
            stats.append(f"**Overall Sentiment**: {overall} ({compound:+.3f})")

        if keywords:
            top_keyword = keywords[0][0] if keywords else "N/A"
            stats.append(f"**Top Keyword**: {top_keyword}")

        if trends:
            freq = trends.get("frequency", {})
            avg_per_day = freq.get("avg_per_day", 0)
            stats.append(f"**Avg Activity**: {avg_per_day} items/day")

        sections.append(" | ".join(stats))
        sections.append("\n")
        return "\n".join(sections)

    def _build_sentiment_section(self, sentiment: Dict[str, Any]) -> str:
        """Build sentiment analysis section."""
        sections = []
        sections.append("\n## 😊 Sentiment Analysis\n")

        overall = sentiment.get("overall", "Unknown")
        compound = sentiment.get("average_compound", 0.0)
        dist = sentiment.get("distribution", {})

        sections.append(f"**Overall Sentiment**: {overall} (compound score: {compound:+.3f})\n")

        # Distribution
        pos = dist.get("positive", {})
        neu = dist.get("neutral", {})
        neg = dist.get("negative", {})

        sections.append("**Distribution**:\n")

        # ASCII bar chart
        pos_pct = pos.get("percentage", 0)
        neu_pct = neu.get("percentage", 0)
        neg_pct = neg.get("percentage", 0)

        # Create bars (1 block = 2%)
        pos_bars = "█" * int(pos_pct / 2)
        neu_bars = "█" * int(neu_pct / 2)
        neg_bars = "█" * int(neg_pct / 2)

        sections.append(f"- Positive: {pos_bars} {pos_pct:.1f}% ({pos.get('count', 0)} items)")
        sections.append(f"- Neutral:  {neu_bars} {neu_pct:.1f}% ({neu.get('count', 0)} items)")
        sections.append(f"- Negative: {neg_bars} {neg_pct:.1f}% ({neg.get('count', 0)} items)")

        sections.append(f"\n*Analyzed {sentiment.get('total_analyzed', 0)} items*\n")
        return "\n".join(sections)

    def _build_keywords_section(self, keywords: List[tuple]) -> str:
        """Build top keywords section."""
        sections = []
        sections.append("\n## 🔑 Top Keywords\n")

        if not keywords:
            sections.append("*No keywords extracted*\n")
            return "\n".join(sections)

        # Show top 15 keywords
        sections.append("**Most Important Topics**:\n")

        for i, (keyword, score) in enumerate(keywords[:15], 1):
            # Lower score = more important in YAKE
            importance = "🔥" if i <= 5 else "📌" if i <= 10 else "•"
            sections.append(f"{importance} {keyword}")

        sections.append(f"\n*Extracted {len(keywords)} total keywords*\n")
        return "\n".join(sections)

    def _build_trends_section(self, trends: Dict[str, Any]) -> str:
        """Build temporal trends section."""
        sections = []
        sections.append("\n## 📈 Temporal Trends\n")

        # Date range
        date_range = trends.get("date_range", {})
        start = date_range.get("start", "Unknown")
        end = date_range.get("end", "Unknown")

        sections.append(f"**Date Range**: {start} to {end}\n")

        # Frequency stats
        freq = trends.get("frequency", {})
        sections.append("**Activity Frequency**:")
        sections.append(f"- Average: {freq.get('avg_per_day', 0)} items/day")
        sections.append(f"- Peak: {freq.get('max_per_day', 0)} items/day")
        sections.append(f"- Coverage: {freq.get('total_days', 0)} days\n")

        # Engagement trends (if available)
        engagement = trends.get("engagement_trends", {})
        if engagement.get("available"):
            sections.append("**Engagement Trends** (X/Twitter):")
            sections.append(f"- Average Likes: {engagement.get('avg_likes', 0)}")
            sections.append(f"- Average Retweets: {engagement.get('avg_retweets', 0)}")
            sections.append(f"- Average Replies: {engagement.get('avg_replies', 0)}")
            sections.append(f"- Total Engagement: {engagement.get('total_engagement', 0):,}\n")

        # Timeline (show last 7 days)
        timeline = trends.get("timeline", [])
        if timeline:
            sections.append("**Recent Activity**:")
            for entry in timeline[-7:]:  # Last 7 days
                date = entry.get("date")
                count = entry.get("count")
                sections.append(f"- {date}: {count} items")

        sections.append("")
        return "\n".join(sections)

    def _build_comparison_section(self, comparison: Dict[str, Any]) -> str:
        """Build comparison with previous report section."""
        sections = []
        sections.append("\n## 🔄 Changes Since Last Report\n")

        # New topics
        new_topics = comparison.get("new_topics", [])
        if new_topics:
            sections.append("**New Topics**:")
            for topic in new_topics[:5]:
                sections.append(f"- ✨ {topic}")
            sections.append("")

        # Removed topics
        removed_topics = comparison.get("removed_topics", [])
        if removed_topics:
            sections.append("**Declining Topics**:")
            for topic in removed_topics[:5]:
                sections.append(f"- 📉 {topic}")
            sections.append("")

        # Sentiment changes
        sentiment_change = comparison.get("sentiment_change", {})
        if sentiment_change:
            old_sent = sentiment_change.get("old", "Unknown")
            new_sent = sentiment_change.get("new", "Unknown")
            direction = sentiment_change.get("direction", "→")
            sections.append(f"**Sentiment Shift**: {old_sent} {direction} {new_sent}\n")

        # Trend direction
        trend_direction = comparison.get("trend_direction", "")
        if trend_direction:
            sections.append(f"**Overall Trend**: {trend_direction}\n")

        return "\n".join(sections)
