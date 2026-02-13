# Changelog

All notable changes to Research Agent will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2026-02-13

### Added - Report Quality Improvements
- Sentiment analysis using VADER (`src/analyzers/sentiment_analyzer.py`)
- Keyword extraction using YAKE (`src/analyzers/keyword_extractor.py`)
- Temporal trend analysis (`src/analyzers/trend_analyzer.py`)
- Quick Stats Dashboard in reports
- Sentiment Analysis section with ASCII bar charts
- Top Keywords section with importance indicators
- Temporal Trends section with timeline and engagement stats

### Added - Better Error Handling
- Enhanced retry logic with exponential backoff using tenacity
- Partial results support with `--allow-partial` flag (default: True)
- Error reporting utility with troubleshooting suggestions (`src/utils/error_reporter.py`)
- Error categorization (auth, rate limit, network, timeout)
- Error logging to files for debugging
- Graceful degradation when sources fail

### Added - Comparison Analysis
- Report parser for existing markdown reports (`src/parsers/report_parser.py`)
- Comparison analyzer (`src/analyzers/comparison_analyzer.py`)
- `--compare-with` CLI option to compare with previous reports
- Comparison section in reports showing new/removed topics and sentiment shifts

### Added - Interactive Mode
- Interactive session manager (`src/interactive/session.py`)
- Follow-up question analyzer (`src/interactive/followup_analyzer.py`)
- Prompt templates for interactive mode (`src/interactive/prompts.py`)
- `--interactive` CLI flag
- Special commands: focus, sentiment, keywords, sources, help
- Conversation history tracking
- Conversation export to markdown

### Added - Testing & Documentation
- Comprehensive test suite (`test_enhancements.py`)
- Feature documentation (`ENHANCEMENTS.md`)
- Implementation summary (`IMPLEMENTATION_SUMMARY.md`)
- Quick start guide (`QUICK_START.md`)

### Changed
- Modified `src/main.py` to integrate all new features
- Enhanced `src/generators/markdown_generator.py` with new report sections
- Updated `src/analyzers/claude_analyzer.py` to support custom prompts
- Updated `src/analyzers/gemini_analyzer.py` to support custom prompts
- Enhanced `src/collectors/base.py` with advanced retry mechanisms

### Dependencies Added
- `tenacity>=8.2.0` - Advanced retry logic
- `vaderSentiment>=3.3.2` - Sentiment analysis
- `yake>=0.4.8` - Keyword extraction
- `prompt_toolkit>=3.0.0` - Interactive CLI

### Fixed
- Python 3.9 compatibility (replaced `|` union syntax with `Optional`)

### Security
- Error logs exclude sensitive information
- API keys remain secure in .env file only

## [0.1.0] - 2025-02-12

### Added
- Initial release
- MVP features complete
