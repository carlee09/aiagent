"""Main CLI entry point for Research Agent."""

import sys
from pathlib import Path
from datetime import datetime
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from src.config import Config
from src.collectors import XCollector, WebCollector
from src.analyzers import ClaudeAnalyzer, GeminiAnalyzer
from src.analyzers.sentiment_analyzer import SentimentAnalyzer
from src.analyzers.keyword_extractor import KeywordExtractor
from src.analyzers.trend_analyzer import TrendAnalyzer
from src.generators import MarkdownGenerator
from src.utils import get_logger, validate_topic, validate_sources, validate_depth
from src.utils.validators import validate_max_items
from src.utils.error_reporter import ErrorReporter

console = Console()
logger = get_logger("main")


@click.command()
@click.option(
    "--topic",
    required=True,
    help="Research topic to investigate",
    callback=lambda ctx, param, value: validate_topic(value) if value else None
)
@click.option(
    "--sources",
    default=Config.DEFAULT_SOURCES,
    help="Data sources to use: x, web, or all (default: all)",
    callback=lambda ctx, param, value: validate_sources(value)
)
@click.option(
    "--max-items",
    default=Config.DEFAULT_MAX_ITEMS,
    type=int,
    help=f"Maximum items to collect per source (default: {Config.DEFAULT_MAX_ITEMS})",
    callback=lambda ctx, param, value: validate_max_items(value)
)
@click.option(
    "--output",
    default=None,
    help="Output filename (default: auto-generated)",
    type=str
)
@click.option(
    "--depth",
    default=Config.DEFAULT_DEPTH,
    help="Analysis depth: quick or detailed (default: detailed)",
    callback=lambda ctx, param, value: validate_depth(value)
)
@click.option(
    "--model",
    default=Config.DEFAULT_MODEL,
    type=click.Choice(["claude", "gemini"], case_sensitive=False),
    help=f"AI model to use: claude or gemini (default: {Config.DEFAULT_MODEL})"
)
@click.option(
    "--allow-partial",
    is_flag=True,
    default=True,
    help="Allow partial results if some sources fail (default: True)"
)
@click.option(
    "--compare-with",
    default=None,
    help="Previous report to compare with (file path)",
    type=str
)
@click.option(
    "--interactive",
    is_flag=True,
    help="Enter interactive mode after analysis"
)
@click.version_option(version="0.1.0", prog_name="Research Agent")
def cli(topic: str, sources: list, max_items: int, output: str, depth: str, model: str,
        allow_partial: bool, compare_with: str, interactive: bool):
    """
    Research Agent - AI-powered research automation tool.

    Automatically collects data from X and web search, analyzes it with AI,
    and generates comprehensive Markdown reports.

    Example:

        research-agent --topic "AI agents 2024"

        research-agent --topic "Anthropic Claude" --sources x,web --max-items 30 --model gemini
    """
    console.print("\n[bold cyan]🔬 Research Agent[/bold cyan]")
    console.print(f"[dim]Topic: {topic}[/dim]")
    console.print(f"[dim]Sources: {', '.join(sources)}[/dim]")
    console.print(f"[dim]Max items per source: {max_items}[/dim]")
    console.print(f"[dim]Analysis depth: {depth}[/dim]")
    console.print(f"[dim]AI Model: {model}[/dim]\n")

    try:
        # Validate configuration
        Config.validate(model=model)
        Config.ensure_output_dir()

        # Initialize components
        collectors = {
            "x": XCollector() if "x" in sources else None,
            "web": WebCollector() if "web" in sources else None,
        }

        # Select analyzer based on model choice
        if model.lower() == "claude":
            analyzer = ClaudeAnalyzer()
            model_display = "Claude AI"
        else:  # gemini
            analyzer = GeminiAnalyzer()
            model_display = "Gemini AI"

        generator = MarkdownGenerator()

        # Step 1: Collect data with error tracking
        all_data = []
        collection_errors = []
        successful_sources = []
        failed_sources = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console
        ) as progress:

            if collectors["x"]:
                task = progress.add_task(
                    f"🔍 Collecting X data... (0/{max_items})",
                    total=max_items
                )
                try:
                    x_data = collectors["x"].collect(topic, max_items)
                    all_data.extend(x_data)
                    progress.update(task, completed=len(x_data))

                    if len(x_data) > 0:
                        console.print(f"[green]✓[/green] Collected {len(x_data)} X posts")
                        successful_sources.append("X")
                    else:
                        console.print(f"[yellow]⚠️[/yellow]  No X data collected")
                        failed_sources.append("X")
                except Exception as e:
                    collection_errors.append(("X", e))
                    failed_sources.append("X")
                    console.print(f"[red]✗[/red] X collection failed: {str(e)[:50]}")
                    logger.error(f"X collection error: {e}", exc_info=True)

                    # Log error details
                    ErrorReporter.log_error_to_file("X", e, {
                        "topic": topic,
                        "max_items": max_items
                    })

            if collectors["web"]:
                task = progress.add_task(
                    f"🌐 Collecting web data... (0/{max_items})",
                    total=max_items
                )
                try:
                    web_data = collectors["web"].collect(topic, max_items)
                    all_data.extend(web_data)
                    progress.update(task, completed=len(web_data))

                    if len(web_data) > 0:
                        console.print(f"[green]✓[/green] Collected {len(web_data)} web results")
                        successful_sources.append("Web")
                    else:
                        console.print(f"[yellow]⚠️[/yellow]  No web data collected")
                        failed_sources.append("Web")
                except Exception as e:
                    collection_errors.append(("Web", e))
                    failed_sources.append("Web")
                    console.print(f"[red]✗[/red] Web collection failed: {str(e)[:50]}")
                    logger.error(f"Web collection error: {e}", exc_info=True)

                    # Log error details
                    ErrorReporter.log_error_to_file("Web", e, {
                        "topic": topic,
                        "max_items": max_items
                    })

        # Handle collection results
        if not all_data:
            console.print("\n[red]❌ No data collected from any source.[/red]")

            # Show troubleshooting suggestions
            if collection_errors:
                console.print("\n[yellow]💡 Troubleshooting suggestions:[/yellow]")
                for source, error in collection_errors:
                    suggestions = ErrorReporter.suggest_fixes(error)
                    for suggestion in suggestions[:3]:  # Show top 3 suggestions
                        console.print(f"  • {suggestion}")

            sys.exit(1)

        # Show partial success warning if applicable
        if failed_sources and allow_partial:
            console.print(f"\n[yellow]⚠️  Partial collection:[/yellow] {len(successful_sources)}/{len(sources)} sources succeeded")
            console.print(f"[dim]  Successful: {', '.join(successful_sources)}[/dim]")
            console.print(f"[dim]  Failed: {', '.join(failed_sources)}[/dim]")
        elif failed_sources and not allow_partial:
            console.print(f"\n[red]❌ Some sources failed and --allow-partial is disabled[/red]")
            sys.exit(1)

        console.print(f"\n[cyan]Total items collected: {len(all_data)}[/cyan]\n")

        # Step 2: Enhanced Analysis (sentiment, keywords, trends)
        sentiment_results = None
        keywords = None
        trends = None

        with console.status("[bold cyan]🔍 Running enhanced analysis...[/bold cyan]"):
            try:
                # Sentiment analysis
                sentiment_analyzer = SentimentAnalyzer()
                sentiment_results = sentiment_analyzer.analyze_items(all_data)
                console.print(f"[green]✓[/green] Sentiment: {sentiment_results.get('overall', 'Unknown')}")

                # Keyword extraction
                keyword_extractor = KeywordExtractor()
                keywords = keyword_extractor.extract_keywords(all_data, top_n=20)
                console.print(f"[green]✓[/green] Extracted {len(keywords)} keywords")

                # Trend analysis
                trend_analyzer = TrendAnalyzer()
                trends = trend_analyzer.analyze_temporal_trends(all_data)
                console.print(f"[green]✓[/green] Analyzed trends across {trends.get('total_dates', 0)} dates")

            except Exception as e:
                logger.warning(f"Enhanced analysis failed: {e}")
                console.print(f"[yellow]⚠️[/yellow]  Enhanced analysis partially failed, continuing...")

        console.print("")

        # Step 3: Analyze with AI
        with console.status(f"[bold yellow]🤖 Analyzing with {model_display}...[/bold yellow]"):
            analysis_result = analyzer.analyze(topic, all_data, depth)

        if not analysis_result.get("success"):
            console.print(f"[red]❌ Analysis failed: {analysis_result.get('error')}[/red]")
            sys.exit(1)

        metadata = analysis_result.get("metadata", {})
        console.print(f"[green]✓[/green] Analysis completed")
        console.print(f"[dim]  Tokens used: {metadata.get('tokens_used', 'N/A')}[/dim]\n")

        # Step 4: Comparison analysis (if requested)
        comparison_result = None
        if compare_with:
            with console.status("[bold cyan]🔄 Comparing with previous report...[/bold cyan]"):
                try:
                    from src.parsers.report_parser import ReportParser
                    from src.analyzers.comparison_analyzer import ComparisonAnalyzer

                    parser = ReportParser()
                    previous_report = parser.parse_report(Path(compare_with))

                    comparator = ComparisonAnalyzer()
                    comparison_result = comparator.compare_analyses(
                        current={
                            "sentiment": sentiment_results,
                            "keywords": keywords,
                            "analysis": analysis_result
                        },
                        previous=previous_report
                    )

                    console.print(f"[green]✓[/green] Comparison complete")

                except Exception as e:
                    logger.warning(f"Comparison analysis failed: {e}")
                    console.print(f"[yellow]⚠️[/yellow]  Comparison failed: {e}")

        # Step 5: Generate report
        with console.status("[bold yellow]📝 Generating report...[/bold yellow]"):
            # Determine output path
            if output:
                output_path = Config.OUTPUT_DIR / output
                if not output_path.suffix:
                    output_path = output_path.with_suffix(".md")
            else:
                filename = generator.generate_filename(topic)
                output_path = Config.OUTPUT_DIR / filename

            # Organize sources
            sources_organized = analyzer.summarize_sources(all_data)

            # Generate report with enhanced features
            success = generator.generate_report(
                topic,
                analysis_result,
                sources_organized,
                output_path,
                sentiment=sentiment_results,
                keywords=keywords,
                trends=trends,
                comparison=comparison_result
            )

        if success:
            console.print(f"[green]✓[/green] Report generated successfully!\n")
            console.print(f"[bold]📄 Report saved to:[/bold] [cyan]{output_path}[/cyan]\n")
            console.print("[dim]You can open it with any Markdown viewer or editor.[/dim]")
        else:
            console.print("[red]❌ Failed to generate report[/red]")
            sys.exit(1)

        # Step 6: Interactive mode (if requested)
        if interactive:
            try:
                from src.interactive import InteractiveSession

                console.print("\n" + "="*60)
                console.print("[bold cyan]🎯 Entering Interactive Mode[/bold cyan]")
                console.print("="*60)
                console.print("\nYou can now ask follow-up questions about the research.")
                console.print("Type 'help' for available commands or 'exit' to quit.\n")

                session = InteractiveSession(
                    topic=topic,
                    data=all_data,
                    analysis=analysis_result,
                    analyzer=analyzer,
                    sentiment=sentiment_results,
                    keywords=keywords,
                    trends=trends
                )

                while True:
                    try:
                        # Get user input
                        user_input = console.input("[bold green]You:[/bold green] ").strip()

                        if not user_input:
                            continue

                        if user_input.lower() in ["exit", "quit", "q"]:
                            console.print("\n[yellow]👋 Exiting interactive mode...[/yellow]")
                            break

                        # Process question
                        response = session.ask_question(user_input)
                        console.print(f"\n[bold blue]Assistant:[/bold blue]\n{response}\n")

                    except KeyboardInterrupt:
                        console.print("\n\n[yellow]👋 Exiting interactive mode...[/yellow]")
                        break
                    except EOFError:
                        console.print("\n\n[yellow]👋 Exiting interactive mode...[/yellow]")
                        break

                # Offer to export conversation
                if session.conversation_history:
                    export = console.input("\n[cyan]Save conversation? (y/n):[/cyan] ").strip().lower()
                    if export == 'y':
                        conv_filename = f"conversation_{topic.replace(' ', '-')[:30]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                        conv_path = Config.OUTPUT_DIR / conv_filename
                        if session.export_conversation(str(conv_path)):
                            console.print(f"[green]✓[/green] Conversation saved to: {conv_path}")

            except Exception as e:
                logger.error(f"Interactive mode error: {e}", exc_info=True)
                console.print(f"[red]❌ Interactive mode failed: {e}[/red]")

    except ValueError as e:
        console.print(f"[red]❌ Configuration error: {e}[/red]")
        console.print("\n[yellow]💡 Tip:[/yellow] Make sure to:")
        console.print("  1. Copy .env.example to .env")
        console.print("  2. Add your API keys to .env file")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n\n[yellow]⚠️  Operation cancelled by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        console.print(f"[red]❌ Unexpected error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    cli()
