# Research Agent 🔬

> **Version 2.0.0** - AI-powered research automation with advanced analytics and interactive features

AI-powered research automation and analysis tool that helps researchers focus on insights instead of data collection.

## Overview

**Research Agent** automatically collects data from X (Twitter) and web search, analyzes it with AI (Claude or Gemini), and generates comprehensive Markdown research reports with **advanced sentiment analysis, keyword extraction, temporal trends, and interactive follow-up capabilities**.

### Key Features

- 🤖 **Multiple AI Models**: Choose between Claude Sonnet 4 or Google Gemini
- 🔍 **Multi-Source Collection**: Automated data gathering from X and web
- 📊 **Advanced Analytics**: Sentiment analysis, keyword extraction, and trend analysis
- 💡 **Smart Error Handling**: Partial results support and intelligent retry logic
- 🔄 **Comparison Analysis**: Track changes between reports over time
- 💬 **Interactive Mode**: Ask follow-up questions without re-collecting data
- 📝 **Enhanced Reports**: Beautiful Markdown reports with charts and insights
- ⚡ **Fast & Efficient**: Research in minutes, not hours
- 🎯 **Flexible Options**: Customizable sources, depth, model, and output

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/research-agent.git
cd research-agent

# Check Python version (must be 3.10+)
python3 --version

# If Python < 3.10, install a newer version:
# macOS: brew install python@3.12
# Ubuntu/Debian: sudo apt install python3.12
# Windows: Download from python.org

# Create virtual environment with Python 3.10+
python3.10 -m venv venv  # or python3.11, python3.12
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:
```bash
# At least one AI model API key is required
GEMINI_API_KEY=your-gemini-key-here          # Recommended
ANTHROPIC_API_KEY=sk-ant-your-key-here       # Optional

# Sela Network API (for X and web search)
SELA_API_KEY=your-sela-key-here
SELA_API_ENDPOINT=https://api.selanetwork.io/api/rpc/scrapeUrl

# Default AI model (claude or gemini)
DEFAULT_MODEL=gemini
```

## 🎉 What's New in v2.0.0

Research Agent has been **significantly enhanced** with powerful new features:

- **📊 Advanced Analytics**: Every report includes sentiment analysis, keyword extraction, and trend analysis
- **💬 Interactive Mode**: Ask follow-up questions without re-collecting data (`--interactive`)
- **🔄 Comparison**: Track changes over time by comparing reports (`--compare-with`)
- **🛡️ Robust Error Handling**: Continues with partial data when sources fail (`--allow-partial`)
- **📈 Visual Insights**: ASCII charts and visualizations in reports
- **🎯 Smart Retry Logic**: Automatic exponential backoff for failed requests

[Read the full changelog →](CHANGELOG.md)

### Usage

Basic usage (with all enhanced features):
```bash
research-agent --topic "AI agents 2024"
```

With model selection:
```bash
# Use Gemini (default)
research-agent --topic "AI agents 2024" --model gemini

# Use Claude
research-agent --topic "AI agents 2024" --model claude
```

Advanced usage:
```bash
research-agent \
  --topic "Anthropic Claude updates" \
  --sources x,web \
  --max-items 30 \
  --model gemini \
  --output claude-research.md \
  --depth detailed
```

## CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--topic` | Research topic (required) | - |
| `--sources` | Data sources: `x`, `web`, or `all` | `all` |
| `--max-items` | Maximum items per source | `20` |
| `--model` | AI model: `claude` or `gemini` | `gemini` |
| `--output` | Output filename | Auto-generated |
| `--depth` | Analysis depth: `quick` or `detailed` | `detailed` |
| `--allow-partial` | Allow partial results if some sources fail | `True` |
| `--compare-with` | Previous report to compare with (file path) | - |
| `--interactive` | Enter interactive mode after analysis | `False` |

## Examples

### Example 1: Market Research with Gemini
```bash
research-agent --topic "AI coding assistants market 2024" \
  --sources all \
  --max-items 30 \
  --model gemini
```

**Result**: Comprehensive market analysis with trends, competitors, and user sentiment.

### Example 2: Academic Research with Claude
```bash
research-agent --topic "Large Language Models safety" \
  --sources web \
  --max-items 50 \
  --model claude \
  --depth detailed
```

**Result**: Detailed academic analysis with latest papers and research findings.

### Example 3: Social Media Trend Analysis
```bash
research-agent --topic "sustainable fashion trends" \
  --sources x \
  --max-items 40 \
  --model gemini
```

**Result**: Social media trends and influencer opinions on sustainable fashion.

### Example 4: Comparison Analysis (v2.0+)
```bash
# First report
research-agent --topic "ethereum" --output eth_week1.md

# Compare with new data
research-agent --topic "ethereum" \
  --output eth_week2.md \
  --compare-with output/eth_week1.md
```

**Result**: Shows what changed - new topics, sentiment shifts, and trend direction.

### Example 5: Interactive Research Session (v2.0+)
```bash
research-agent --topic "AI safety concerns" \
  --sources x,web \
  --max-items 20 \
  --interactive
```

**Then ask:**
```
You: What are the main concerns mentioned?
You: Show me positive opinions only
You: Focus on regulation
You: exit
```

**Result**: Get instant answers without re-collecting data.

## 🆕 New Features (v2.0.0)

### Sentiment Analysis & Insights
Every report now includes automatic sentiment analysis with distribution charts:

```bash
research-agent --topic "product launch reactions"
```

**You get:**
- Overall sentiment (Positive/Neutral/Negative)
- Distribution breakdown with ASCII charts
- Compound sentiment score

### Keyword Extraction
Automatically extracts and ranks the top 20 keywords:

```bash
research-agent --topic "AI trends 2024"
```

**You get:**
- 🔥 Most important topics
- 📌 Secondary themes
- Relevance scoring

### Comparison Analysis
Compare current research with previous reports:

```bash
research-agent --topic "bitcoin" --compare-with reports/bitcoin_last_week.md
```

**You get:**
- New topics that emerged
- Topics that declined
- Sentiment shifts
- Trend direction

### Interactive Mode
Ask follow-up questions without re-collecting data:

```bash
research-agent --topic "AI safety" --interactive
```

**Then ask:**
- "What are the main concerns?"
- "Show me positive opinions only"
- "Focus on regulation"
- Type `help` for all commands

### Smart Error Handling
Collections continue even when sources fail:

```bash
research-agent --topic "niche topic" --allow-partial
```

**Benefits:**
- Automatic retry with exponential backoff
- Partial results when one source fails
- Clear error messages with suggestions
- Never lose all data due to one failure

## AI Models

### Google Gemini (Recommended)
- **Model**: `gemini-2.5-flash`
- **Pros**: Fast, cost-effective, high quality
- **Best for**: General research, quick analysis, high-volume usage
- **Get API Key**: [Google AI Studio](https://makersuite.google.com/app/apikey)

### Anthropic Claude
- **Model**: `claude-sonnet-4-20250514`
- **Pros**: Exceptional reasoning, detailed analysis
- **Best for**: Complex research, academic work, in-depth analysis
- **Get API Key**: [Anthropic Console](https://console.anthropic.com/)

You can switch between models anytime using the `--model` option!

## Report Structure

Generated reports include:

### Enhanced Analytics (v2.0+)
- **📊 Quick Stats Dashboard**: Overall sentiment, top keyword, activity stats
- **😊 Sentiment Analysis**: Distribution with visual charts (Positive/Neutral/Negative)
- **🔑 Top Keywords**: Most important topics ranked by relevance
- **📈 Temporal Trends**: Timeline, engagement stats, and activity frequency
- **🔄 Comparison** (optional): Changes since previous report

### AI Analysis
- **Executive Summary**: Key findings in 3-5 sentences
- **Key Insights**: Major discoveries with evidence
- **Detailed Analysis**: Thematic breakdown of findings
- **Opinion Analysis**: Mainstream vs. contrasting views
- **Conclusion**: Recommendations and next steps

### Data Sources
- **X (Twitter)**: Posts with engagement metrics (or N/A if unavailable)
- **Web**: Articles with source and date information

See [examples/sample_report.md](examples/sample_report.md) or the generated test report for examples.

## Project Structure

```
research-agent/
├── src/
│   ├── main.py              # CLI entry point
│   ├── config.py            # Configuration management
│   ├── collectors/          # Data collection
│   │   ├── base.py          # Base with retry logic
│   │   ├── x_collector.py   # X API integration
│   │   └── web_collector.py # Web search integration
│   ├── analyzers/           # AI & Enhanced analysis
│   │   ├── claude_analyzer.py      # Claude integration
│   │   ├── gemini_analyzer.py      # Gemini integration
│   │   ├── sentiment_analyzer.py   # Sentiment analysis (NEW)
│   │   ├── keyword_extractor.py    # Keyword extraction (NEW)
│   │   ├── trend_analyzer.py       # Trend analysis (NEW)
│   │   ├── comparison_analyzer.py  # Report comparison (NEW)
│   │   └── prompt_templates.py
│   ├── parsers/             # Report parsing (NEW)
│   │   └── report_parser.py # Parse existing reports
│   ├── interactive/         # Interactive mode (NEW)
│   │   ├── session.py       # Session management
│   │   ├── followup_analyzer.py
│   │   └── prompts.py
│   ├── generators/          # Report generation
│   │   └── markdown_generator.py  # Enhanced reports
│   └── utils/              # Utilities
│       ├── logger.py
│       ├── validators.py
│       └── error_reporter.py      # Error handling (NEW)
├── examples/               # Sample files
├── tests/                 # Test suite
├── output/                # Generated reports
└── docs/                  # Documentation
    ├── ENHANCEMENTS.md
    ├── QUICK_START.md
    └── IMPLEMENTATION_SUMMARY.md
```

## Requirements

- **Python 3.10+ (REQUIRED)** - Python 3.9 is past its end-of-life and no longer supported
- At least one AI API key:
  - Google Gemini API key (recommended), OR
  - Anthropic Claude API key
- Sela Network API key (for X and web search)

### ⚠️ Important: Python Version
Python 3.9 reached end-of-life and is no longer receiving updates. The dependencies (google-auth, google-genai) will only provide critical bug fixes for Python 3.9 on a best-effort basis. **Please upgrade to Python 3.10 or later.**

### Dependencies (v2.0.0)
The following packages are automatically installed:
- `click` - CLI framework
- `anthropic` - Claude AI
- `google-generativeai` - Gemini AI
- `requests` - HTTP client
- `rich` - Beautiful terminal output
- `tenacity` - Advanced retry logic
- `vaderSentiment` - Sentiment analysis
- `yake` - Keyword extraction
- `prompt_toolkit` - Interactive CLI

## API Setup

### Google Gemini API (Recommended)

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add to `.env` as `GEMINI_API_KEY`
4. **Free tier available** with generous limits

### Anthropic Claude API (Optional)

1. Sign up at [console.anthropic.com](https://console.anthropic.com/)
2. Create an API key
3. Add to `.env` as `ANTHROPIC_API_KEY`
4. Pay-as-you-go pricing

### Sela Network API

1. Contact Sela Network for API access
2. Obtain API key and endpoint URL
3. Add to `.env`:
   - `SELA_API_KEY`
   - `SELA_API_ENDPOINT`

**Supported Scrape Types:**
- `GOOGLE_SEARCH`: Google search results
- `TWITTER_PROFILE`: Twitter user profile posts
- `TWITTER_POST`: Individual tweet scraping

See [SELA_API.md](SELA_API.md) for detailed API documentation and request/response formats.

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint
flake8 src/ tests/

# Type check
mypy src/
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Roadmap

### ✅ Completed (v2.0.0) - February 2026
- [x] CLI interface with Click
- [x] X and Web data collection
- [x] Claude AI integration
- [x] Gemini AI integration
- [x] Markdown report generation
- [x] Multi-model support
- [x] **Sentiment analysis with VADER**
- [x] **Keyword extraction with YAKE**
- [x] **Temporal trend analysis**
- [x] **Enhanced error handling with retry logic**
- [x] **Partial results support**
- [x] **Report comparison and change tracking**
- [x] **Interactive mode with follow-up questions**
- [x] **ASCII charts and visualizations**

### Phase 2 (Next 3 months)
- [ ] Scheduled research automation
- [ ] PDF and HTML export
- [ ] Additional AI models (GPT-4, etc.)
- [ ] Email notifications
- [ ] Advanced visualizations (graphs, charts)

### Phase 3 (6 months)
- [ ] Team collaboration features
- [ ] Web dashboard
- [ ] Real-time monitoring
- [ ] Custom data source plugins
- [ ] API mode for integration

## Troubleshooting

### "No AI API key found"
Make sure you have at least one of these in your `.env`:
- `GEMINI_API_KEY` (recommended)
- `ANTHROPIC_API_KEY`

### "SELA_API_KEY is required"
Add your Sela Network API credentials to `.env`:
```bash
SELA_API_KEY=your-key-here
SELA_API_ENDPOINT=https://api.selanetwork.io/api/rpc/scrapeUrl
```

### Python version warnings
**Python 3.9 is no longer supported.** You must use Python 3.10 or later. To upgrade:

```bash
# 1. Install Python 3.10+ (if not already installed)
# macOS (Homebrew):
brew install python@3.12

# Ubuntu/Debian:
sudo apt update
sudo apt install python3.12 python3.12-venv

# Windows: Download from https://www.python.org/downloads/

# 2. Remove old virtual environment
rm -rf venv

# 3. Create new virtual environment with Python 3.10+
python3.12 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 4. Reinstall dependencies
pip install -r requirements.txt
pip install -e .
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Documentation

### Quick Links
- **[QUICK_START.md](QUICK_START.md)** - Get started in 5 minutes
- **[ENHANCEMENTS.md](ENHANCEMENTS.md)** - Detailed feature documentation
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Technical details
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

### Testing
Run the test suite to verify all features:
```bash
# Test core features
python test_enhancements.py

# Test report generation
python test_report_generation.py

# Test N/A fallback for missing data
python test_na_fallback.py
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Support

- 📖 [Documentation](https://github.com/yourusername/research-agent/wiki)
- 🐛 [Report Issues](https://github.com/yourusername/research-agent/issues)
- 💬 [Discussions](https://github.com/yourusername/research-agent/discussions)

## Acknowledgments

- Powered by [Anthropic Claude](https://anthropic.com/) & [Google Gemini](https://ai.google.dev/)
- Data collection via [Sela Network](https://selanetwork.io)
- Built with [Click](https://click.palletsprojects.com/) and [Rich](https://rich.readthedocs.io/)

---

**Research Agent** - Automate your research, amplify your insights. 🚀
