"""Gemini AI analyzer for research data."""

from typing import Dict, Any, List
from google import genai

from src.config import Config
from src.utils.logger import get_logger
from .prompt_templates import get_analysis_prompt


class GeminiAnalyzer:
    """Analyzer using Google Gemini AI for research data analysis."""

    def __init__(self):
        """Initialize Gemini analyzer."""
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self.logger = get_logger(self.__class__.__name__)

    def analyze(
        self,
        topic: str,
        data_items: List[Dict[str, Any]],
        depth: str = "detailed",
        custom_prompt: str = None
    ) -> Dict[str, Any]:
        """
        Analyze collected research data using Gemini AI.

        Args:
            topic: Research topic
            data_items: List of collected data items
            depth: Analysis depth (quick or detailed)
            custom_prompt: Optional custom prompt (for interactive mode)

        Returns:
            Dictionary containing analysis results
        """
        self.logger.info(f"🤖 Analyzing {len(data_items)} items with Gemini AI...")

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

            # Call Gemini API with new client
            response = self.client.models.generate_content(
                model=Config.GEMINI_MODEL,
                contents=prompt,
                config={
                    'max_output_tokens': Config.GEMINI_MAX_TOKENS,
                    'temperature': Config.GEMINI_TEMPERATURE,
                }
            )

            # Extract analysis from response
            analysis_text = response.text

            # Count tokens (approximate)
            # Gemini doesn't provide exact token counts in the same way as Claude
            prompt_tokens = len(prompt.split()) * 1.3  # rough estimate
            completion_tokens = len(analysis_text.split()) * 1.3
            total_tokens = int(prompt_tokens + completion_tokens)

            self.logger.info("✅ Analysis completed successfully")

            return {
                "success": True,
                "analysis": analysis_text,
                "metadata": {
                    "model": Config.GEMINI_MODEL,
                    "tokens_used": total_tokens,  # approximate
                    "depth": depth,
                    "items_analyzed": len(data_items)
                }
            }

        except Exception as e:
            self.logger.error(f"❌ Gemini API error: {e}")
            return {
                "success": False,
                "error": f"Gemini API error: {str(e)}",
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
