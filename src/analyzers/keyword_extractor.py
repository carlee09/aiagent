"""Keyword extraction for research data."""

from typing import List, Tuple, Dict, Any
import yake
from collections import Counter
from src.utils.logger import get_logger


class KeywordExtractor:
    """Extracts keywords from collected data using YAKE."""

    def __init__(self):
        """Initialize keyword extractor."""
        self.logger = get_logger(self.__class__.__name__)

        # Configure YAKE keyword extractor
        # Parameters: language, max_ngram_size, deduplication_threshold, num_of_keywords
        self.extractor = yake.KeywordExtractor(
            lan="en",
            n=2,  # Max 2-word phrases
            dedupLim=0.7,  # Similarity threshold for deduplication
            top=20,  # Extract top 20 keywords
            features=None
        )

    def extract_keywords(
        self,
        data_items: List[Dict[str, Any]],
        top_n: int = 20
    ) -> List[Tuple[str, float]]:
        """
        Extract top keywords from all data items.

        Args:
            data_items: List of data items
            top_n: Number of top keywords to return

        Returns:
            List of (keyword, score) tuples, lower score = more important
        """
        if not data_items:
            return []

        self.logger.info(f"Extracting keywords from {len(data_items)} items")

        # Combine all text content
        all_text = []
        for item in data_items:
            content = item.get("content", "") or item.get("title", "")
            if content:
                all_text.append(content)

        if not all_text:
            return []

        # Join all text
        combined_text = " ".join(all_text)

        try:
            # Extract keywords using YAKE
            keywords = self.extractor.extract_keywords(combined_text)

            # YAKE returns (keyword, score) where lower score = more important
            # Limit to top_n results
            result = keywords[:top_n]

            self.logger.info(f"Extracted {len(result)} keywords")
            return result

        except Exception as e:
            self.logger.error(f"Error extracting keywords: {e}")
            return []

    def get_keyword_categories(
        self,
        keywords: List[Tuple[str, float]]
    ) -> Dict[str, List[str]]:
        """
        Group keywords by theme/category (simple heuristic).

        Args:
            keywords: List of (keyword, score) tuples

        Returns:
            Dictionary mapping category to keywords
        """
        if not keywords:
            return {}

        categories = {
            "technology": [],
            "business": [],
            "finance": [],
            "general": []
        }

        # Simple keyword categorization based on common terms
        tech_terms = {
            "ai", "blockchain", "crypto", "web3", "nft", "defi", "protocol",
            "smart contract", "ethereum", "bitcoin", "token", "wallet",
            "network", "platform", "technology", "app", "software", "data"
        }

        business_terms = {
            "company", "business", "market", "ceo", "founder", "partnership",
            "acquisition", "launch", "growth", "users", "customers", "team"
        }

        finance_terms = {
            "price", "trading", "investment", "funding", "revenue", "profit",
            "valuation", "market cap", "exchange", "liquidity", "yield", "apy"
        }

        for keyword, score in keywords:
            keyword_lower = keyword.lower()

            # Check each category
            categorized = False

            if any(term in keyword_lower for term in tech_terms):
                categories["technology"].append(keyword)
                categorized = True

            if any(term in keyword_lower for term in business_terms):
                categories["business"].append(keyword)
                categorized = True

            if any(term in keyword_lower for term in finance_terms):
                categories["finance"].append(keyword)
                categorized = True

            if not categorized:
                categories["general"].append(keyword)

        # Remove empty categories
        return {k: v for k, v in categories.items() if v}

    def get_keyword_frequency(
        self,
        data_items: List[Dict[str, Any]],
        keywords: List[Tuple[str, float]]
    ) -> Dict[str, int]:
        """
        Calculate frequency of keywords in the data.

        Args:
            data_items: List of data items
            keywords: List of (keyword, score) tuples

        Returns:
            Dictionary mapping keyword to frequency count
        """
        if not data_items or not keywords:
            return {}

        # Combine all text
        all_text = " ".join([
            (item.get("content", "") or item.get("title", "")).lower()
            for item in data_items
        ])

        # Count keyword occurrences
        frequency = {}
        for keyword, score in keywords:
            count = all_text.count(keyword.lower())
            frequency[keyword] = count

        return frequency

    def format_keywords_for_display(
        self,
        keywords: List[Tuple[str, float]],
        max_display: int = 15
    ) -> str:
        """
        Format keywords as a text-based visualization.

        Args:
            keywords: List of (keyword, score) tuples
            max_display: Maximum keywords to display

        Returns:
            Formatted string for display
        """
        if not keywords:
            return "No keywords extracted"

        # Normalize scores to sizes (1-5)
        scores = [score for _, score in keywords[:max_display]]
        if not scores:
            return "No keywords extracted"

        min_score = min(scores)
        max_score = max(scores)
        score_range = max_score - min_score if max_score > min_score else 1

        formatted = []
        for keyword, score in keywords[:max_display]:
            # Invert score (lower is better in YAKE)
            # Normalize to 1-5 range
            if score_range > 0:
                size = 5 - int(((score - min_score) / score_range) * 4)
            else:
                size = 3

            # Different formatting based on importance
            if size >= 4:
                formatted.append(f"**{keyword}**")  # Most important
            elif size >= 3:
                formatted.append(f"*{keyword}*")    # Important
            else:
                formatted.append(keyword)            # Less important

        return ", ".join(formatted)
