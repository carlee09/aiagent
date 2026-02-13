# Research Agent - Enhanced Features

This document describes the new features added to the Research Agent in the latest update.

## 🎯 Overview

The Research Agent has been significantly enhanced with four major feature sets:

1. **Report Quality Improvements** - Sentiment analysis, keyword extraction, and trend analysis
2. **Better Error Handling** - Retry logic, fallback mechanisms, and partial results support
3. **Comparison Analysis** - Compare current research with previous reports
4. **Interactive Mode** - Ask follow-up questions after initial analysis

---

## 1. Report Quality Improvements

### Features

#### Sentiment Analysis
- Uses VADER sentiment analysis (lightweight, no training needed)
- Analyzes sentiment for each data item
- Provides overall sentiment distribution (positive/neutral/negative)
- Shows sentiment trends over time

#### Keyword Extraction
- Uses YAKE for unsupervised keyword extraction
- Extracts top 20 keywords from all content
- Calculates keyword importance and frequency
- Groups keywords by theme

#### Trend Analysis
- Groups data by date to identify temporal patterns
- Tracks engagement trends for X posts
- Calculates posting frequency statistics
- Shows timeline of activity

### Enhanced Reports Include:

**Quick Stats Dashboard**
- Overall sentiment with compound score
- Top keyword
- Average activity per day

**Sentiment Analysis Section**
- Overall sentiment (Positive/Neutral/Negative)
- Distribution breakdown with ASCII visualization
- Compound score

**Top Keywords Section**
- Most important topics ranked by relevance
- Keyword importance indicators (🔥 📌 •)

**Temporal Trends Section**
- Date range of data
- Activity frequency statistics
- Engagement trends (for X posts)
- Timeline of recent activity

### Usage

All enhanced features are automatically enabled. Just run the agent normally:

```bash
research-agent --topic "your topic"
```

The generated report will include all enhancement sections.

---

## 2. Better Error Handling

### Features

#### Enhanced Retry Logic
- Exponential backoff with jitter
- Configurable retry strategies (default: 5 attempts)
- Circuit breaker pattern for repeated failures
- Smart error categorization (auth, rate limit, network, timeout)

#### Partial Results Support
- Collections continue even if one source fails
- Displays which sources succeeded/failed
- Shows collection success rate
- Only fails if ALL sources fail

#### Error Reporting
- Detailed error messages with context
- Troubleshooting suggestions based on error type
- Error logging to files for debugging
- Clear warnings vs. fatal errors

### Usage

**Allow Partial Results** (enabled by default):
```bash
research-agent --topic "your topic" --allow-partial
```

**Require All Sources**:
```bash
research-agent --topic "your topic" --no-allow-partial
```

### Error Suggestions

The agent provides helpful suggestions when errors occur:
- API authentication issues → Check .env file
- Rate limits → Reduce --max-items or wait
- Network errors → Check connection
- Timeouts → Reduce --max-items

---

## 3. Comparison Analysis

### Features

#### Report Comparison
- Parse existing markdown reports
- Compare sentiment changes
- Identify new vs. removed topics
- Calculate trend direction
- Show what's changed since last report

#### Comparison Sections
- **Changes Since Last Report** - New and declining topics
- **Sentiment Shifts** - How sentiment has changed
- **Trend Direction** - Overall trend indicators

### Usage

```bash
research-agent --topic "uniswap" --compare-with "reports/previous_report.md"
```

The generated report will include a comparison section showing:
- New topics that emerged
- Topics that are declining
- Sentiment changes (e.g., Positive → Negative)
- Overall trend direction

### Example Output

```markdown
## 🔄 Changes Since Last Report

**New Topics**:
- ✨ Uniswap v4 hooks
- ✨ Smart contract upgrades
- ✨ BlackRock integration

**Declining Topics**:
- 📉 Uniswap v3 features
- 📉 Legacy protocols

**Sentiment Shift**: Neutral ↗️ Positive

**Overall Trend**: Sentiment improving | Many new topics emerging
```

---

## 4. Interactive Mode

### Features

#### Follow-up Questions
- Ask questions about the research without re-collecting data
- AI-powered answers using existing data
- Context-aware responses
- Conversation history tracking

#### Available Commands

**General Questions**:
```
> What are the main concerns about Uniswap v4?
> Show me positive opinions only
> How has sentiment changed over time?
```

**Special Commands**:
- `focus <topic>` - Deep dive on a specific topic
- `sentiment` - Show detailed sentiment breakdown
- `keywords` - Show all extracted keywords
- `sources` - Show data sources summary
- `help` or `?` - Show help message
- `exit` or `quit` - Exit interactive mode

#### Conversation Export
- Save interactive session to markdown file
- Includes all questions and answers
- Timestamped for reference

### Usage

```bash
research-agent --topic "uniswap" --interactive
```

After the initial analysis completes, you'll enter interactive mode:

```
============================================================
🎯 Entering Interactive Mode
============================================================

You can now ask follow-up questions about the research.
Type 'help' for available commands or 'exit' to quit.

You: What are the negative opinions about Uniswap v4?