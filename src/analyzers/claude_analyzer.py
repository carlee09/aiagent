"""Claude AI analyzer for research data."""

from typing import Dict, Any, List
import anthropic

from src.config import Config
from src.utils.logger import get_logger
from .prompt_templates import get_analysis_prompt


class ClaudeAnalyzer:
    """Analyzer using Claude AI for research data analysis."""

    def __init__(self):
        """Initialize Claude analyzer."""
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        self.logger = get_logger(self.__class__.__name__)

    def analyze(
        self,
        topic: str,
        data_items: List[Dict[str, Any]],
        depth: str = "detailed",
        custom_prompt: str = None
    ) -> Dict[str, Any]:
        """
        Analyze collected research data using Claude AI.

        Args:
            topic: Research topic
            data_items: List of collected data items
            depth: Analysis depth (quick or detailed)
            custom_prompt: Optional custom prompt (for interactive mode)

        Returns:
            Dictionary containing analysis results
        """
        self.logger.info(f"🤖 Analyzing {len(data_items)} items with Claude AI...")

        if not data_items:
            self.logger.warning("⚠️  No data to analyze")
            return {
                "success": False,
                "error": "No data collected",
                "analysis": None
            }

        try:
            # Generate prompt (use custom if provided)
            if custom_prompt:
                prompt = custom_prompt
            else:
                prompt = get_analysis_prompt(topic, data_items, depth)

            # Call Claude API
            response = self.client.messages.create(
                model=Config.CLAUDE_MODEL,
                max_tokens=Config.CLAUDE_MAX_TOKENS,
                temperature=Config.CLAUDE_TEMPERATURE,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract analysis from response
            analysis_text = response.content[0].text

            self.logger.info("✅ Analysis completed successfully")

            return {
                "success": True,
                "analysis": analysis_text,
                "metadata": {
                    "model": Config.CLAUDE_MODEL,
                    "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
                    "depth": depth,
                    "items_analyzed": len(data_items)
                }
            }

        except anthropic.APIError as e:
            self.logger.error(f"❌ Claude API error: {e}")
            return {
                "success": False,
                "error": f"Claude API error: {str(e)}",
                "analysis": None
            }
        except Exception as e:
            self.logger.error(f"❌ Unexpected error during analysis: {e}")
            return {
                "success": False,
                "error": f"Analysis error: {str(e)}",
                "analysis": None
            }

    def summarize_sources(self, data_items: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, str]]]:
        """
        Organize and summarize data sources.

        Args:
            data_items: List of collected data items

        Returns:
            Dictionary with organized sources by type
        """
        sources = {
            "x": [],
            "web": []
        }

        for item in data_items:
            source_type = item.get("source", "unknown")

            if source_type == "x":
                sources["x"].append({
                    "author": item.get("author", ""),
                    "content": item.get("content", "")[:200] + "...",
                    "date": item.get("date", ""),
                    "url": item.get("url", ""),
                    "engagement": item.get("engagement", {})
                })
            elif source_type == "web":
                sources["web"].append({
                    "title": item.get("title", ""),
                    "source": item.get("author", ""),
                    "date": item.get("date", ""),
                    "url": item.get("url", "")
                })

        return sources
