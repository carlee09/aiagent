"""Follow-up question analyzer."""

from typing import Dict, List, Any
from src.utils.logger import get_logger
from src.interactive.prompts import build_followup_prompt


logger = get_logger("followup_analyzer")


class FollowupAnalyzer:
    """Analyzes follow-up questions using existing data."""

    def __init__(self, analyzer: Any):
        """
        Initialize follow-up analyzer.

        Args:
            analyzer: AI analyzer instance (ClaudeAnalyzer or GeminiAnalyzer)
        """
        self.analyzer = analyzer
        self.logger = logger

    def analyze_question(
        self,
        question: str,
        data: List[Dict[str, Any]],
        original_analysis: Dict[str, Any],
        context: Dict[str, Any] = None
    ) -> str:
        """
        Analyze a follow-up question using existing data.

        Args:
            question: User's question
            data: Collected data items
            original_analysis: Original analysis results
            context: Additional context (topic, sentiment, etc.)

        Returns:
            Answer to the question
        """
        self.logger.info(f"Analyzing follow-up question: {question[:50]}...")

        try:
            # Extract relevant data for the question
            relevant_data = self.extract_relevant_data(question, data)

            if not relevant_data:
                # Use all data if no specific matches
                relevant_data = data

            # Limit data to prevent token overflow
            limited_data = relevant_data[:30]  # Max 30 items

            # Build follow-up prompt
            prompt = build_followup_prompt(
                question=question,
                data=limited_data,
                original_analysis=original_analysis.get("analysis", ""),
                context=context or {}
            )

            # Use the analyzer's analyze method with the custom prompt
            # For quick follow-ups, use "quick" depth
            result = self.analyzer.analyze(
                topic=question,
                data=limited_data,
                depth="quick",
                custom_prompt=prompt
            )

            if result.get("success"):
                return result.get("analysis", "No answer generated")
            else:
                return f"❌ Analysis failed: {result.get('error', 'Unknown error')}"

        except Exception as e:
            self.logger.error(f"Error analyzing question: {e}")
            return f"❌ Error: {str(e)}"

    def extract_relevant_data(
        self,
        question: str,
        all_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Extract data items relevant to the question.

        Args:
            question: User's question
            all_data: All collected data

        Returns:
            List of relevant data items
        """
        question_lower = question.lower()

        # Extract key terms from question
        # Simple keyword matching for now
        relevant = []

        for item in all_data:
            content = (item.get("content", "") or item.get("title", "")).lower()

            # Check if any word from question appears in content
            # (Simple approach - could be enhanced with NLP)
            question_words = set(
                word for word in question_lower.split()
                if len(word) > 3 and word not in {
                    "what", "how", "why", "when", "where", "show", "tell",
                    "about", "the", "are", "is", "was", "were", "been", "have",
                    "has", "had", "do", "does", "did", "will", "would", "could",
                    "should", "may", "might", "can", "this", "that", "these",
                    "those", "and", "or", "but", "for", "with"
                }
            )

            # Count matching words
            matches = sum(1 for word in question_words if word in content)

            if matches > 0:
                relevant.append((item, matches))

        # Sort by relevance (number of matches)
        relevant.sort(key=lambda x: x[1], reverse=True)

        # Return just the items (not the match counts)
        return [item for item, _ in relevant]

    def refine_analysis(
        self,
        focus_area: str,
        data: List[Dict[str, Any]],
        original_analysis: str
    ) -> str:
        """
        Refine analysis to focus on a specific area.

        Args:
            focus_area: Area to focus on
            data: Data items
            original_analysis: Original analysis text

        Returns:
            Refined analysis
        """
        question = f"Focus specifically on {focus_area} and provide detailed insights."

        return self.analyze_question(
            question=question,
            data=data,
            original_analysis={"analysis": original_analysis}
        )
