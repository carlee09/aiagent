"""Test script for enhanced features."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.analyzers.sentiment_analyzer import SentimentAnalyzer
from src.analyzers.keyword_extractor import KeywordExtractor
from src.analyzers.trend_analyzer import TrendAnalyzer


def test_sentiment_analyzer():
    """Test sentiment analysis."""
    print("="*60)
    print("Testing Sentiment Analyzer")
    print("="*60)

    # Mock data
    test_data = [
        {"content": "This is amazing! I love this product.", "source": "x"},
        {"content": "This is the worst experience ever.", "source": "x"},
        {"content": "It's okay, nothing special.", "source": "web"},
        {"content": "Absolutely fantastic! Highly recommend.", "source": "x"},
        {"content": "Terrible service and poor quality.", "source": "web"},
    ]

    analyzer = SentimentAnalyzer()
    results = analyzer.analyze_items(test_data)

    print(f"\nOverall Sentiment: {results['overall']}")
    print(f"Average Compound: {results['average_compound']:.3f}")
    print("\nDistribution:")
    for category, data in results['distribution'].items():
        print(f"  {category.capitalize()}: {data['percentage']:.1f}% ({data['count']} items)")

    print("\n✓ Sentiment analysis test passed!")
    return results


def test_keyword_extractor():
    """Test keyword extraction."""
    print("\n" + "="*60)
    print("Testing Keyword Extractor")
    print("="*60)

    # Mock data
    test_data = [
        {"content": "Uniswap v4 introduces new hooks for customization", "source": "web"},
        {"content": "The new Uniswap protocol offers better liquidity", "source": "x"},
        {"content": "DeFi protocols like Uniswap are revolutionizing finance", "source": "web"},
        {"content": "Smart contracts on Ethereum enable Uniswap", "source": "x"},
        {"content": "Liquidity pools and automated market makers", "source": "web"},
    ]

    extractor = KeywordExtractor()
    keywords = extractor.extract_keywords(test_data, top_n=10)

    print(f"\nExtracted {len(keywords)} keywords:")
    for i, (keyword, score) in enumerate(keywords, 1):
        print(f"  {i}. {keyword} (score: {score:.4f})")

    print("\n✓ Keyword extraction test passed!")
    return keywords


def test_trend_analyzer():
    """Test trend analysis."""
    print("\n" + "="*60)
    print("Testing Trend Analyzer")
    print("="*60)

    # Mock data with dates
    test_data = [
        {"content": "Post 1", "source": "x", "date": "2024-01-15", "engagement": {"likes": 100, "retweets": 20}},
        {"content": "Post 2", "source": "x", "date": "2024-01-15", "engagement": {"likes": 50, "retweets": 10}},
        {"content": "Post 3", "source": "x", "date": "2024-01-16", "engagement": {"likes": 200, "retweets": 40}},
        {"content": "Article 1", "source": "web", "date": "2024-01-16"},
        {"content": "Article 2", "source": "web", "date": "2024-01-17"},
    ]

    analyzer = TrendAnalyzer()
    results = analyzer.analyze_temporal_trends(test_data)

    print(f"\nDate Range: {results['date_range']['start']} to {results['date_range']['end']}")
    print(f"Total Days: {results['frequency']['total_days']}")
    print(f"Avg per Day: {results['frequency']['avg_per_day']}")

    if results['engagement_trends']['available']:
        eng = results['engagement_trends']
        print(f"\nEngagement Stats:")
        print(f"  Avg Likes: {eng['avg_likes']}")
        print(f"  Avg Retweets: {eng['avg_retweets']}")

    print("\nTimeline:")
    for entry in results['timeline']:
        print(f"  {entry['date']}: {entry['count']} items (avg engagement: {entry['avg_engagement']})")

    print("\n✓ Trend analysis test passed!")
    return results


def test_all():
    """Run all tests."""
    print("\n" + "="*60)
    print("TESTING ENHANCED FEATURES")
    print("="*60 + "\n")

    try:
        # Test sentiment analysis
        sentiment = test_sentiment_analyzer()

        # Test keyword extraction
        keywords = test_keyword_extractor()

        # Test trend analysis
        trends = test_trend_analyzer()

        print("\n" + "="*60)
        print("ALL TESTS PASSED! ✓")
        print("="*60 + "\n")

        print("Summary:")
        print(f"  - Sentiment: {sentiment['overall']} ({sentiment['average_compound']:+.3f})")
        print(f"  - Keywords: {len(keywords)} extracted")
        print(f"  - Trends: {trends['frequency']['total_days']} days analyzed")

        return True

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_all()
    sys.exit(0 if success else 1)
