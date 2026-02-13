"""Error reporting and troubleshooting utility."""

from typing import Dict, List, Any
from datetime import datetime
from pathlib import Path
from src.utils.logger import get_logger

logger = get_logger("error_reporter")


class ErrorReporter:
    """Reports errors and suggests troubleshooting steps."""

    ERROR_SUGGESTIONS = {
        "api_auth": [
            "Check that your API key is correctly set in .env file",
            "Verify the API key hasn't expired",
            "Ensure there are no extra spaces in the API key",
        ],
        "api_rate_limit": [
            "Wait a few minutes before retrying",
            "Consider reducing --max-items value",
            "Check your API quota/usage limits",
        ],
        "network": [
            "Check your internet connection",
            "Try again in a few moments",
            "Check if the API service is experiencing downtime",
        ],
        "invalid_response": [
            "The API returned unexpected data format",
            "Try with a different topic or search term",
            "Check if the service has updated their API",
        ],
        "timeout": [
            "The request took too long to complete",
            "Try reducing --max-items value",
            "Check your network connection speed",
        ],
    }

    @staticmethod
    def report_collection_error(source: str, error: Exception) -> str:
        """
        Format a collection error with context.

        Args:
            source: Name of the data source (e.g., 'X', 'Web')
            error: The exception that occurred

        Returns:
            Formatted error message
        """
        error_type = ErrorReporter._categorize_error(error)
        error_msg = str(error)

        report = f"❌ {source} collection failed: {error_msg}"
        return report

    @staticmethod
    def suggest_fixes(error: Exception) -> List[str]:
        """
        Suggest troubleshooting steps based on error type.

        Args:
            error: The exception that occurred

        Returns:
            List of suggested fixes
        """
        error_type = ErrorReporter._categorize_error(error)
        return ErrorReporter.ERROR_SUGGESTIONS.get(error_type, [
            "Review the error message above",
            "Check your configuration in .env file",
            "Try running with --help for usage information",
        ])

    @staticmethod
    def _categorize_error(error: Exception) -> str:
        """
        Categorize error type based on exception.

        Args:
            error: The exception to categorize

        Returns:
            Error category string
        """
        error_str = str(error).lower()
        error_type_name = type(error).__name__.lower()

        if "auth" in error_str or "401" in error_str or "403" in error_str:
            return "api_auth"
        elif "rate limit" in error_str or "429" in error_str:
            return "api_rate_limit"
        elif "timeout" in error_str or "timed out" in error_str:
            return "timeout"
        elif "network" in error_str or "connection" in error_str:
            return "network"
        elif "invalid" in error_str or "json" in error_str:
            return "invalid_response"
        else:
            return "unknown"

    @staticmethod
    def log_error_to_file(source: str, error: Exception, context: Dict[str, Any]):
        """
        Log error details to a file for debugging.

        Args:
            source: Name of the data source
            error: The exception that occurred
            context: Additional context (topic, max_items, etc.)
        """
        try:
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = log_dir / f"error_{source.lower()}_{timestamp}.log"

            with open(log_file, "w", encoding="utf-8") as f:
                f.write(f"Error Report - {source}\n")
                f.write(f"Timestamp: {datetime.now()}\n")
                f.write(f"\nContext:\n")
                for key, value in context.items():
                    f.write(f"  {key}: {value}\n")
                f.write(f"\nError Type: {type(error).__name__}\n")
                f.write(f"Error Message: {str(error)}\n")

            logger.debug(f"Error details logged to: {log_file}")

        except Exception as e:
            logger.warning(f"Could not write error log: {e}")

    @staticmethod
    def format_partial_success_message(
        successful_sources: List[str],
        failed_sources: List[str],
        total_items: int
    ) -> str:
        """
        Format a message for partial collection success.

        Args:
            successful_sources: List of sources that succeeded
            failed_sources: List of sources that failed
            total_items: Total items collected from successful sources

        Returns:
            Formatted message
        """
        msg_parts = []

        if successful_sources:
            msg_parts.append(
                f"✓ Successfully collected {total_items} items from: {', '.join(successful_sources)}"
            )

        if failed_sources:
            msg_parts.append(
                f"⚠️  Failed to collect from: {', '.join(failed_sources)}"
            )

        return " | ".join(msg_parts)
