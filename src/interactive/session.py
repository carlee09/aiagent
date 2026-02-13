"""Interactive session manager for follow-up questions."""

from typing import Dict, List, Any
from rich.console import Console
from src.utils.logger import get_logger
from src.interactive.followup_analyzer import FollowupAnalyzer
from src.interactive.prompts import build_followup_prompt


console = Console()
logger = get_logger("interactive_session")


class InteractiveSession:
    """Manages interactive session for follow-up questions."""

    def __init__(
        self,
        topic: str,
        data: List[Dict[str, Any]],
        analysis: Dict[str, Any],
        analyzer: Any,  # ClaudeAnalyzer or GeminiAnalyzer
        sentiment: Dict[str, Any] = None,
        keywords: List[tuple] = None,
        trends: Dict[str, Any] = None
    ):
        """
        Initialize interactive session.

        Args:
            topic: Research topic
            data: Collected data items
            analysis: Initial analysis results
            analyzer: AI analyzer instance
            sentiment: Sentiment analysis results
            keywords: Keyword extraction results
            trends: Trend analysis results
        """
        self.topic = topic
        self.data = data
        self.analysis = analysis
        self.analyzer = analyzer
        self.sentiment = sentiment
        self.keywords = keywords
        self.trends = trends

        self.followup_analyzer = FollowupAnalyzer(analyzer)
        self.conversation_history = []

        logger.info(f"Interactive session started for topic: {topic}")

    def ask_question(self, question: str) -> str:
        """
        Process a follow-up question.

        Args:
            question: User's question

        Returns:
            Answer to the question
        """
        logger.info(f"Processing question: {question}")

        try:
            # Handle special commands
            if question.lower() in ["help", "?"]:
                return self._show_help()

            if question.lower().startswith("focus "):
                focus_topic = question[6:].strip()
                return self._focus_on_topic(focus_topic)

            if question.lower() == "sentiment":
                return self._show_sentiment_details()

            if question.lower() == "sources":
                return self._show_sources()

            if question.lower() == "keywords":
                return self._show_keywords()

            # General question - use AI analyzer
            with console.status("[bold yellow]🤖 Thinking...[/bold yellow]"):
                answer = self.followup_analyzer.analyze_question(
                    question=question,
                    data=self.data,
                    original_analysis=self.analysis,
                    context={
                        "topic": self.topic,
                        "sentiment": self.sentiment,
                        "keywords": self.keywords,
                        "trends": self.trends
                    }
                )

            # Store in conversation history
            self.conversation_history.append({
                "question": question,
                "answer": answer
            })

            return answer

        except Exception as e:
            logger.error(f"Error processing question: {e}")
            return f"❌ Error processing question: {str(e)}"

    def _show_help(self) -> str:
        """Show help message with available commands."""
        help_text = """
**Interactive Mode Commands**:

- **Ask any question** - Get AI-powered answers about the research
- **focus <topic>** - Deep dive on a specific topic
- **sentiment** - Show detailed sentiment breakdown
- **keywords** - Show all extracted keywords
- **sources** - Show data sources summary
- **help** or **?** - Show this help message
- **exit** or **quit** - Exit interactive mode

**Example Questions**:
- "What are the main concerns about [topic]?"
- "How has sentiment changed over time?"
- "What are people saying about [specific aspect]?"
- "Show me positive opinions only"
"""
        return help_text.strip()

    def _focus_on_topic(self, focus_topic: str) -> str:
        """
        Deep dive on a specific topic.

        Args:
            focus_topic: Topic to focus on

        Returns:
            Focused analysis
        """
        logger.info(f"Focusing on topic: {focus_topic}")

        # Filter data relevant to the focus topic
        relevant_data = self.followup_analyzer.extract_relevant_data(
            focus_topic,
            self.data
        )

        if not relevant_data:
            return f"❌ No data found related to '{focus_topic}'"

        # Generate focused analysis
        question = f"Provide a detailed analysis focusing specifically on {focus_topic}. Include key points, sentiment, and any notable insights."

        with console.status(f"[bold cyan]🔍 Analyzing {focus_topic}...[/bold cyan]"):
            answer = self.followup_analyzer.analyze_question(
                question=question,
                data=relevant_data,
                original_analysis=self.analysis,
                context={"topic": focus_topic}
            )

        return f"**Focus: {focus_topic}** (found {len(relevant_data)} relevant items)\n\n{answer}"

    def _show_sentiment_details(self) -> str:
        """Show detailed sentiment breakdown."""
        if not self.sentiment:
            return "❌ Sentiment analysis not available"

        overall = self.sentiment.get("overall", "Unknown")
        compound = self.sentiment.get("average_compound", 0.0)
        dist = self.sentiment.get("distribution", {})

        lines = [
            "**Detailed Sentiment Analysis**:\n",
            f"Overall: {overall} (compound: {compound:+.3f})\n",
            "**Distribution**:"
        ]

        for category in ["positive", "neutral", "negative"]:
            cat_data = dist.get(category, {})
            count = cat_data.get("count", 0)
            pct = cat_data.get("percentage", 0)
            lines.append(f"- {category.capitalize()}: {pct:.1f}% ({count} items)")

        # Show examples if available
        lines.append("\nTo see specific examples, ask:")
        lines.append('- "Show me positive opinions"')
        lines.append('- "What are the negative concerns?"')

        return "\n".join(lines)

    def _show_keywords(self) -> str:
        """Show all extracted keywords."""
        if not self.keywords:
            return "❌ Keywords not available"

        lines = [
            "**All Extracted Keywords**:\n",
            f"Total: {len(self.keywords)} keywords\n"
        ]

        # Group into importance levels
        top_tier = self.keywords[:5]
        mid_tier = self.keywords[5:15]
        rest = self.keywords[15:]

        if top_tier:
            lines.append("**Most Important** (🔥):")
            for kw, score in top_tier:
                lines.append(f"  🔥 {kw}")

        if mid_tier:
            lines.append("\n**Important** (📌):")
            for kw, score in mid_tier:
                lines.append(f"  📌 {kw}")

        if rest:
            lines.append(f"\n**Other Topics** ({len(rest)} more):")
            for kw, score in rest[:10]:  # Show only first 10
                lines.append(f"  • {kw}")

        return "\n".join(lines)

    def _show_sources(self) -> str:
        """Show data sources summary."""
        x_count = sum(1 for item in self.data if item.get("source") == "x")
        web_count = sum(1 for item in self.data if item.get("source") == "web")

        lines = [
            "**Data Sources Summary**:\n",
            f"Total Items: {len(self.data)}",
            f"- X (Twitter): {x_count} posts",
            f"- Web: {web_count} articles\n",
            "To explore specific sources, ask:",
            '- "Show me what people are saying on X"',
            '- "What do web articles say?"'
        ]

        return "\n".join(lines)

    def export_conversation(self, output_path: str) -> bool:
        """
        Export conversation history to file.

        Args:
            output_path: Path to save conversation

        Returns:
            True if successful
        """
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"# Interactive Session: {self.topic}\n\n")

                for i, exchange in enumerate(self.conversation_history, 1):
                    f.write(f"## Question {i}\n")
                    f.write(f"{exchange['question']}\n\n")
                    f.write(f"### Answer\n")
                    f.write(f"{exchange['answer']}\n\n")
                    f.write("---\n\n")

            logger.info(f"Conversation exported to: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error exporting conversation: {e}")
            return False
