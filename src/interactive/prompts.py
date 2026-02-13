"""Prompt templates for interactive mode."""

from typing import Dict, List, Any


def build_followup_prompt(
    question: str,
    data: List[Dict[str, Any]],
    original_analysis: str,
    context: Dict[str, Any]
) -> str:
    """
    Build a prompt for follow-up questions.

    Args:
        question: User's question
        data: Relevant data items
        original_analysis: Original analysis text
        context: Additional context

    Returns:
        Formatted prompt string
    """
    # Build data summary
    data_summary = _summarize_data(data)

    # Build context summary
    context_summary = _summarize_context(context)

    prompt = f"""You are analyzing research data to answer a follow-up question.

**Original Topic**: {context.get('topic', 'Unknown')}

**Follow-up Question**: {question}

{context_summary}

**Relevant Data** ({len(data)} items):
{data_summary}

**Original Analysis Summary**:
{original_analysis[:500]}...

**Instructions**:
1. Answer the question directly and concisely
2. Use specific examples from the data to support your answer
3. If the question asks for sentiment, consider both positive and negative aspects
4. If the question asks about trends, look for patterns in the data
5. Keep your response focused on the question - avoid repeating the full original analysis

Provide a clear, focused answer to: "{question}"
"""

    return prompt


def _summarize_data(data: List[Dict[str, Any]]) -> str:
    """Summarize data items for prompt."""
    if not data:
        return "No data available"

    lines = []

    for i, item in enumerate(data[:20], 1):  # Max 20 items for prompt
        source = item.get("source", "unknown")
        content = item.get("content", "") or item.get("title", "")

        # Truncate long content
        if len(content) > 200:
            content = content[:200] + "..."

        # Add engagement info for X posts
        if source == "x":
            engagement = item.get("engagement", {})
            likes = engagement.get("likes", 0)
            lines.append(f"{i}. [X] {content} (👍 {likes})")
        else:
            lines.append(f"{i}. [Web] {content}")

    return "\n".join(lines)


def _summarize_context(context: Dict[str, Any]) -> str:
    """Summarize context for prompt."""
    lines = []

    sentiment = context.get("sentiment")
    if sentiment:
        overall = sentiment.get("overall", "Unknown")
        compound = sentiment.get("average_compound", 0.0)
        lines.append(f"**Overall Sentiment**: {overall} ({compound:+.3f})")

    keywords = context.get("keywords")
    if keywords:
        # Extract just the keyword strings
        if keywords and isinstance(keywords[0], tuple):
            kw_list = [kw[0] for kw in keywords[:10]]
        else:
            kw_list = keywords[:10]
        lines.append(f"**Key Topics**: {', '.join(kw_list)}")

    trends = context.get("trends")
    if trends:
        freq = trends.get("frequency", {})
        avg_per_day = freq.get("avg_per_day", 0)
        lines.append(f"**Activity**: {avg_per_day} items/day average")

    if lines:
        return "\n".join(lines) + "\n"
    else:
        return ""


def build_focus_prompt(topic: str, focus_area: str, data: List[Dict[str, Any]]) -> str:
    """
    Build a prompt for focused analysis.

    Args:
        topic: Main research topic
        focus_area: Specific area to focus on
        data: Relevant data items

    Returns:
        Formatted prompt string
    """
    data_summary = _summarize_data(data)

    prompt = f"""Provide a detailed analysis focusing specifically on: {focus_area}

**Context**: This is part of research on "{topic}"

**Data** ({len(data)} items related to {focus_area}):
{data_summary}

**Instructions**:
1. Focus exclusively on {focus_area}
2. Provide detailed insights and analysis
3. Include specific examples from the data
4. Identify key trends or patterns
5. Note any concerns or positive aspects

Provide a comprehensive analysis of {focus_area}:
"""

    return prompt


def build_sentiment_detail_prompt(data: List[Dict[str, Any]], sentiment_type: str) -> str:
    """
    Build a prompt for detailed sentiment analysis.

    Args:
        data: Data items
        sentiment_type: Type of sentiment to focus on (positive/negative/neutral)

    Returns:
        Formatted prompt string
    """
    data_summary = _summarize_data(data)

    prompt = f"""Analyze the {sentiment_type} sentiment in the following data:

**Data** ({len(data)} items):
{data_summary}

**Instructions**:
1. Focus on {sentiment_type} aspects
2. Provide specific examples
3. Explain why these items are {sentiment_type}
4. Summarize the main {sentiment_type} themes

Provide a detailed {sentiment_type} sentiment analysis:
"""

    return prompt
