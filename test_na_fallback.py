"""Test N/A fallback for engagement data."""

from pathlib import Path
from src.generators.markdown_generator import MarkdownGenerator

print("🧪 Testing N/A Fallback for Likes")
print("="*60)

# Mock data with 0 likes (API returned no engagement data)
mock_sources = {
    "x": [
        {
            "author": "user1",
            "content": "Post with NO engagement data (0 likes)",
            "date": "2024-01-15",
            "url": "https://twitter.com/test/1",
            "engagement": {"likes": 0, "retweets": 0, "replies": 0}  # All zeros
        },
        {
            "author": "user2",
            "content": "Post with SOME engagement data",
            "date": "2024-01-15",
            "url": "https://twitter.com/test/2",
            "engagement": {"likes": 150, "retweets": 30, "replies": 10}  # Has data
        },
        {
            "author": "user3",
            "content": "Post with NO engagement object",
            "date": "2024-01-15",
            "url": "https://twitter.com/test/3",
            "engagement": {}  # Empty engagement
        }
    ],
    "web": []
}

analysis_result = {
    "success": True,
    "analysis": "Test analysis content",
    "metadata": {"model": "Test", "tokens_used": 100}
}

generator = MarkdownGenerator()
output_path = Path("output/test_na_fallback.md")

success = generator.generate_report(
    topic="N/A Fallback Test",
    analysis_result=analysis_result,
    sources=mock_sources,
    output_path=output_path
)

if success:
    print(f"\n✓ Report generated: {output_path}")

    # Read and check the output
    content = output_path.read_text()

    print("\n📊 Checking Data Sources section:")
    print("-"*60)

    # Extract X posts section
    import re
    x_section = re.search(r"### X \(Twitter\).*?(?=\n###|\n---|\Z)", content, re.DOTALL)

    if x_section:
        x_text = x_section.group(0)

        # Check each post
        posts = re.findall(r'\d+\. \*\*@(\w+)\*\*.*?\n.*?👍 ([^\s]+) likes', x_text, re.DOTALL)

        for author, likes in posts:
            print(f"\n  @{author}: 👍 {likes} likes")

            if author == "user1":
                if likes == "N/A":
                    print("    ✓ Correctly shows N/A for 0 likes")
                else:
                    print(f"    ✗ Expected N/A but got: {likes}")

            elif author == "user2":
                if likes == "150":
                    print("    ✓ Correctly shows actual like count")
                else:
                    print(f"    ✗ Expected 150 but got: {likes}")

            elif author == "user3":
                if likes == "N/A":
                    print("    ✓ Correctly shows N/A for empty engagement")
                else:
                    print(f"    ✗ Expected N/A but got: {likes}")

        print("\n" + "="*60)
        print("✅ N/A FALLBACK TEST COMPLETE!")
        print("="*60)

    else:
        print("✗ Could not find X posts section")
else:
    print("✗ Report generation failed")
