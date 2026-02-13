"""Parser for existing markdown reports."""

import re
from pathlib import Path
from typing import Dict, List, Any
from src.utils.logger import get_logger


class ReportParser:
    """Parses existing markdown research reports."""

    def __init__(self):
        """Initialize report parser."""
        self.logger = get_logger(self.__class__.__name__)

    def parse_report(self, file_path: Path) -> Dict[str, Any]:
        """
        Parse an existing markdown report.

        Args:
            file_path: Path to the markdown report

        Returns:
            Dictionary with parsed report data
        """
        self.logger.info(f"Parsing report: {file_path}")

        try:
            content = file_path.read_text(encoding="utf-8")

            # Extract metadata
            metadata = self._extract_metadata(content)

            # Extract sentiment
            sentiment = self._extract_sentiment(content)

            # Extract keywords
            keywords = self._extract_keywords(content)

            # Extract sources
            sources = self._extract_sources(content)

            # Extract main analysis
            analysis = self._extract_analysis(content)

            return {
                "metadata": metadata,
                "sentiment": sentiment,
                "keywords": keywords,
                "sources": sources,
                "analysis": analysis,
                "file_path": str(file_path)
            }

        except Exception as e:
            self.logger.error(f"Error parsing report: {e}")
            raise

    def _extract_metadata(self, content: str) -> Dict[str, str]:
        """Extract metadata from report header."""
        metadata = {}

        # Extract generated date
        date_match = re.search(r"\*\*Generated\*\*:\s*(.+)", content)
        if date_match:
            metadata["generated"] = date_match.group(1).strip()

        # Extract data sources
        sources_match = re.search(r"\*\*Data Sources\*\*:\s*(.+)", content)
        if sources_match:
            metadata["data_sources"] = sources_match.group(1).strip()

        # Extract model
        model_match = re.search(r"\*\*Analysis Model\*\*:\s*(.+)", content)
        if model_match:
            metadata["model"] = model_match.group(1).strip()

        return metadata

    def _extract_sentiment(self, content: str) -> Dict[str, Any]:
        """Extract sentiment analysis section."""
        sentiment = {}

        # Look for sentiment section
        sentiment_section = re.search(
            r"## 😊 Sentiment Analysis\s*\n(.+?)(?=\n##|$)",
            content,
            re.DOTALL
        )

        if not sentiment_section:
            return None

        section_text = sentiment_section.group(1)

        # Extract overall sentiment
        overall_match = re.search(r"\*\*Overall Sentiment\*\*:\s*(\w+)", section_text)
        if overall_match:
            sentiment["overall"] = overall_match.group(1)

        # Extract compound score
        compound_match = re.search(r"compound score:\s*([-+]?\d+\.\d+)", section_text)
        if compound_match:
            sentiment["average_compound"] = float(compound_match.group(1))

        # Extract distribution
        distribution = {}

        pos_match = re.search(r"Positive:.*?(\d+\.\d+)%.*?\((\d+) items\)", section_text)
        if pos_match:
            distribution["positive"] = {
                "percentage": float(pos_match.group(1)),
                "count": int(pos_match.group(2))
            }

        neu_match = re.search(r"Neutral:.*?(\d+\.\d+)%.*?\((\d+) items\)", section_text)
        if neu_match:
            distribution["neutral"] = {
                "percentage": float(neu_match.group(1)),
                "count": int(neu_match.group(2))
            }

        neg_match = re.search(r"Negative:.*?(\d+\.\d+)%.*?\((\d+) items\)", section_text)
        if neg_match:
            distribution["negative"] = {
                "percentage": float(neg_match.group(1)),
                "count": int(neg_match.group(2))
            }

        if distribution:
            sentiment["distribution"] = distribution

        return sentiment if sentiment else None

    def _extract_keywords(self, content: str) -> List[str]:
        """Extract keywords from report."""
        keywords = []

        # Look for keywords section
        keywords_section = re.search(
            r"## 🔑 Top Keywords\s*\n(.+?)(?=\n##|$)",
            content,
            re.DOTALL
        )

        if not keywords_section:
            return []

        section_text = keywords_section.group(1)

        # Extract keywords (remove emoji markers)
        keyword_lines = re.findall(r"[🔥📌•]\s*(.+)", section_text)
        keywords = [kw.strip() for kw in keyword_lines if kw.strip()]

        return keywords

    def _extract_sources(self, content: str) -> Dict[str, List[str]]:
        """Extract data sources from report."""
        sources = {"x": [], "web": []}

        # Look for data sources section
        sources_section = re.search(
            r"## 📚 Data Sources\s*\n(.+?)(?=\n##|---|\Z)",
            content,
            re.DOTALL
        )

        if not sources_section:
            return sources

        section_text = sources_section.group(1)

        # Count X posts
        x_match = re.search(r"### X \(Twitter\) - (\d+) posts", section_text)
        if x_match:
            sources["x_count"] = int(x_match.group(1))

        # Count web results
        web_match = re.search(r"### Web - (\d+) results", section_text)
        if web_match:
            sources["web_count"] = int(web_match.group(1))

        return sources

    def _extract_analysis(self, content: str) -> str:
        """Extract main analysis text."""
        # Find content between header and Data Sources section
        analysis_match = re.search(
            r"---\s*\n(.+?)\n## 📚 Data Sources",
            content,
            re.DOTALL
        )

        if analysis_match:
            # Skip enhancement sections if present
            analysis_text = analysis_match.group(1)

            # Remove enhancement sections
            analysis_text = re.sub(
                r"## 📊 Quick Stats.+?(?=\n##|$)",
                "",
                analysis_text,
                flags=re.DOTALL
            )
            analysis_text = re.sub(
                r"## 😊 Sentiment Analysis.+?(?=\n##|$)",
                "",
                analysis_text,
                flags=re.DOTALL
            )
            analysis_text = re.sub(
                r"## 🔑 Top Keywords.+?(?=\n##|$)",
                "",
                analysis_text,
                flags=re.DOTALL
            )
            analysis_text = re.sub(
                r"## 📈 Temporal Trends.+?(?=\n##|$)",
                "",
                analysis_text,
                flags=re.DOTALL
            )
            analysis_text = re.sub(
                r"## 🔄 Changes Since Last Report.+?(?=\n##|$)",
                "",
                analysis_text,
                flags=re.DOTALL
            )

            return analysis_text.strip()

        return ""
