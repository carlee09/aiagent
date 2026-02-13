"""Test enhanced report generation with mock data."""

from pathlib import Path
from src.generators.markdown_generator import MarkdownGenerator
from src.analyzers.sentiment_analyzer import SentimentAnalyzer
from src.analyzers.keyword_extractor import KeywordExtractor
from src.analyzers.trend_analyzer import TrendAnalyzer

# Mock data
mock_data = [
    {
        "content": "Uniswap v4 introduces amazing new hooks! This is fantastic for DeFi.",
        "source": "x",
        "author": "defi_expert",
        "date": "2024-01-15",
        "url": "https://twitter.com/test/1",
        "engagement": {"likes": 150, "retweets": 30, "replies": 10}
    },
    {
        "content": "The new liquidity pools are revolutionary. Great work by the Uniswap team.",
        "source": "x",
        "author": "crypto_trader",
        "date": "2024-01-15",
        "url": "https://twitter.com/test/2",
        "engagement": {"likes": 200, "retweets": 45, "replies": 15}
    },
    {
        "content": "Smart contracts on Uniswap v4 enable powerful customization.",
        "source": "web",
        "title": "Uniswap v4: A Deep Dive",
        "author": "CoinDesk",
        "date": "2024-01-16",
        "url": "https://example.com/article1"
    },
    {
        "content": "Concerned about gas fees with the new protocol. Performance issues noted.",
        "source": "x",
        "author": "eth_watcher",
        "date": "2024-01-16",
        "url": "https://twitter.com/test/3",
        "engagement": {"likes": 80, "retweets": 12, "replies": 25}
    },
    {
        "content": "DeFi protocols like Uniswap are changing the financial landscape forever.",
        "source": "web",
        "title": "The Future of DeFi",
        "author": "Decrypt",
        "date": "2024-01-17",
        "url": "https://example.com/article2"
    }
]

print("🔬 Testing Enhanced Report Generation\n")
print("="*60)

# Run sentiment analysis
print("\n1. Running Sentiment Analysis...")
sentiment_analyzer = SentimentAnalyzer()
sentiment = sentiment_analyzer.analyze_items(mock_data)
print(f"   ✓ Overall: {sentiment['overall']} ({sentiment['average_compound']:+.3f})")

# Extract keywords
print("\n2. Extracting Keywords...")
keyword_extractor = KeywordExtractor()
keywords = keyword_extractor.extract_keywords(mock_data, top_n=10)
print(f"   ✓ Extracted {len(keywords)} keywords")
print(f"   ✓ Top 3: {', '.join([kw[0] for kw in keywords[:3]])}")

# Analyze trends
print("\n3. Analyzing Trends...")
trend_analyzer = TrendAnalyzer()
trends = trend_analyzer.analyze_temporal_trends(mock_data)
print(f"   ✓ Date range: {trends['date_range']['start']} to {trends['date_range']['end']}")
print(f"   ✓ Total days: {trends['frequency']['total_days']}")

# Generate report
print("\n4. Generating Enhanced Report...")
generator = MarkdownGenerator()

# Mock analysis result
analysis_result = {
    "success": True,
    "analysis": """## Executive Summary

Uniswap v4 is receiving positive attention in the DeFi community. The new hooks feature
is particularly well-received, offering developers powerful customization capabilities.

## Key Findings

1. **Innovation**: The v4 upgrade introduces significant innovations in liquidity provision
2. **Community Response**: Generally positive, with some concerns about gas fees
3. **Market Impact**: Expected to strengthen Uniswap's position in the DeFi ecosystem

## Concerns

- Gas fee optimization still needed
- Performance monitoring required for complex hooks

## Outlook

The community is optimistic about v4's potential to revolutionize DeFi interactions.""",
    "metadata": {
        "model": "Claude Sonnet 4",
        "tokens_used": 1234,
        "depth": "detailed"
    }
}

# Organize sources
sources = {
    "x": [
        {
            "author": item["author"],
            "content": item["content"][:200],
            "date": item["date"],
            "url": item["url"],
            "engagement": item.get("engagement", {})
        }
        for item in mock_data if item["source"] == "x"
    ],
    "web": [
        {
            "title": item.get("title", ""),
            "source": item["author"],
            "date": item["date"],
            "url": item["url"]
        }
        for item in mock_data if item["source"] == "web"
    ]
}

output_path = Path("output/test_enhanced_report.md")
success = generator.generate_report(
    topic="Uniswap v4",
    analysis_result=analysis_result,
    sources=sources,
    output_path=output_path,
    sentiment=sentiment,
    keywords=keywords,
    trends=trends
)

if success:
    print(f"   ✓ Report generated: {output_path}")

    # Read and show key sections
    content = output_path.read_text()

    print("\n" + "="*60)
    print("📊 Report Preview - New Sections:")
    print("="*60)

    # Check for new sections
    has_quick_stats = "## 📊 Quick Stats" in content
    has_sentiment = "## 😊 Sentiment Analysis" in content
    has_keywords = "## 🔑 Top Keywords" in content
    has_trends = "## 📈 Temporal Trends" in content

    print(f"\n✓ Quick Stats Section: {'YES ✓' if has_quick_stats else 'NO ✗'}")
    print(f"✓ Sentiment Section: {'YES ✓' if has_sentiment else 'NO ✗'}")
    print(f"✓ Keywords Section: {'YES ✓' if has_keywords else 'NO ✗'}")
    print(f"✓ Trends Section: {'YES ✓' if has_trends else 'NO ✗'}")

    print("\n" + "="*60)
    print("✅ ENHANCED REPORT GENERATION TEST PASSED!")
    print("="*60)
    print(f"\n📄 View the full report at: {output_path}")

else:
    print("   ✗ Report generation failed!")
