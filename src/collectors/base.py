"""Base collector class."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    RetryError
)
import requests
from src.utils.logger import get_logger


class BaseCollector(ABC):
    """Base class for data collectors."""

    def __init__(self, api_key: str, api_url: str):
        """
        Initialize collector.

        Args:
            api_key: API key for authentication
            api_url: Base API URL
        """
        self.api_key = api_key
        self.api_url = api_url
        self.logger = get_logger(self.__class__.__name__)
        self.retry_attempts = 5
        self.retry_min_wait = 2
        self.retry_max_wait = 30

    @abstractmethod
    def collect(self, topic: str, max_items: int = 20) -> List[Dict[str, Any]]:
        """
        Collect data for the given topic.

        Args:
            topic: Research topic
            max_items: Maximum number of items to collect

        Returns:
            List of collected data items
        """
        pass

    def _format_result(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format raw API data into standardized structure.

        Args:
            raw_data: Raw data from API

        Returns:
            Formatted data dictionary
        """
        return {
            "content": raw_data.get("content", ""),
            "author": raw_data.get("author", ""),
            "date": raw_data.get("date", ""),
            "url": raw_data.get("url", ""),
            "metadata": raw_data.get("metadata", {}),
        }

    def _create_retry_decorator(self):
        """
        Create a retry decorator with exponential backoff.

        Returns:
            Configured retry decorator
        """
        return retry(
            stop=stop_after_attempt(self.retry_attempts),
            wait=wait_exponential(
                multiplier=1,
                min=self.retry_min_wait,
                max=self.retry_max_wait
            ),
            retry=retry_if_exception_type((
                requests.exceptions.RequestException,
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError,
            )),
            reraise=True,
            before_sleep=lambda retry_state: self.logger.warning(
                f"Retry attempt {retry_state.attempt_number}/{self.retry_attempts} "
                f"after {retry_state.outcome.exception()}"
            )
        )

    def _fetch_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute a function with retry logic.

        Args:
            func: Function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function

        Returns:
            Function result

        Raises:
            Exception: If all retry attempts fail
        """
        retry_decorator = self._create_retry_decorator()
        retried_func = retry_decorator(func)

        try:
            return retried_func(*args, **kwargs)
        except RetryError as e:
            self.logger.error(f"All retry attempts failed: {e}")
            raise e.last_attempt.exception()

    def _is_retriable_error(self, exception: Exception) -> bool:
        """
        Determine if an error should trigger a retry.

        Args:
            exception: The exception to check

        Returns:
            True if the error is retriable, False otherwise
        """
        # Don't retry authentication errors (401, 403)
        if isinstance(exception, requests.exceptions.HTTPError):
            if exception.response.status_code in [401, 403]:
                return False

        # Retry on network errors, timeouts, and rate limits
        if isinstance(exception, (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException
        )):
            return True

        # Check for rate limit in error message
        error_msg = str(exception).lower()
        if "rate limit" in error_msg or "429" in error_msg:
            return True

        return False
