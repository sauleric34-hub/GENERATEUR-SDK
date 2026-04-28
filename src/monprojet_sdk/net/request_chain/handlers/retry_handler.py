import random

from typing import Generator, Optional, Tuple
from time import sleep
from .base_handler import BaseHandler
from ...transport.request import Request
from ...transport.response import Response
from ...transport.api_error import ApiError
from ...transport.request_error import RequestError


class RetryHandler(BaseHandler):
    """
    Handler for retrying requests.
    Supports configurable retry attempts, exponential backoff with jitter, and specific status codes or HTTP methods to retry.

    :ivar int _max_attempts: The maximum number of retry attempts.
    :ivar int _delay_in_milliseconds: The initial delay between retry attempts in milliseconds.
    :ivar int _max_delay_in_milliseconds: The maximum delay between retry attempts in milliseconds (caps exponential backoff).
    :ivar float _backoff_factor: Multiplier for exponential backoff.
    :ivar int _jitter_in_milliseconds: Maximum random jitter in milliseconds to add to retry delays.
    :ivar set[int] | None _status_codes_to_retry: Specific HTTP status codes to retry (None triggers default: 5xx + 408, 429).
    :ivar set[str] _http_methods_to_retry: HTTP methods that are allowed to be retried.
    """

    def __init__(self):
        """
        Initialize a new instance of RetryHandler.
        """
        super().__init__()
        self._max_attempts = 3
        self._delay_in_milliseconds = 150
        self._max_delay_in_milliseconds = 5000
        self._backoff_factor = 2
        self._jitter_in_milliseconds = 50
        self._status_codes_to_retry = None
        self._http_methods_to_retry = {
            m.upper()
            for m in ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
        }

    def handle(
        self, request: Request
    ) -> Tuple[Optional[Response], Optional[RequestError]]:
        """
        Retry the request based on configured retry settings.
        Implements exponential backoff with optional jitter between retry attempts.
        Per-request retry config (via request.config['retry']) overrides SDK defaults.

        :param Request request: The request to retry.
        :return: The response and any error that occurred.
        :rtype: Tuple[Optional[Response], Optional[RequestError]]
        :raises RequestError: If the handler chain is incomplete.
        """
        if self._next_handler is None:
            raise RequestError("Handler chain is incomplete")

        retry_config = (request.config or {}).get("retry") or {}
        max_attempts = retry_config.get("attempts", self._max_attempts)

        response, error = self._next_handler.handle(request)

        try_count = 0
        while try_count < max_attempts and self._should_retry(error, request):
            self._delay(try_count, request)
            response, error = self._next_handler.handle(request)
            try_count += 1

        return response, error

    def stream(
        self, request: Request
    ) -> Generator[Tuple[Optional[Response], Optional[RequestError]], None, None]:
        """
        Retry the request based on configured retry settings.
        Implements exponential backoff with optional jitter between retry attempts.
        Per-request retry config (via request.config['retry']) overrides SDK defaults.

        :param Request request: The request to retry.
        :return: The response and any error that occurred.
        :rtype: Generator[Tuple[Optional[Response], Optional[RequestError]], None, None]
        :raises RequestError: If the handler chain is incomplete.
        """
        if self._next_handler is None:
            raise RequestError("Handler chain is incomplete")

        try:
            retry_config = (request.config or {}).get("retry") or {}
            max_attempts = retry_config.get("attempts", self._max_attempts)
            try_count = 0
            stream = self._next_handler.stream(request)
            while True:
                response, error = next(stream)
                if try_count < max_attempts and self._should_retry(error, request):
                    self._delay(try_count, request)
                    try_count += 1
                    stream = self._next_handler.stream(request)  # Retry the request
                elif try_count >= max_attempts:
                    yield response, error
                    break
                else:
                    yield response, error

        except StopIteration:
            pass

    def _delay(self, try_count: int, request: Request) -> None:
        """
        Calculate and apply delay before next retry attempt using exponential backoff.
        Delay is capped at maximum delay and optional jitter is added.
        Per-request retry config overrides SDK defaults.

        :param int try_count: Current retry attempt number (0-indexed).
        :param Request request: The request being retried, used to read per-request retry config.
        """
        retry_config = (request.config or {}).get("retry") or {}
        base_delay = retry_config.get("delay_ms", self._delay_in_milliseconds)
        max_delay = retry_config.get("max_delay_ms", self._max_delay_in_milliseconds)
        backoff_factor = retry_config.get("backoff_factor", self._backoff_factor)
        jitter = retry_config.get("jitter_ms", self._jitter_in_milliseconds)

        # Calculate exponential backoff: initialDelay * (backoffFactor ^ try_count)
        delay = base_delay * (backoff_factor**try_count)

        # Cap at max delay
        delay = min(delay, max_delay)

        # Add jitter: random value between 0 and jitter_ms
        if jitter > 0:
            delay += random.uniform(0, jitter)

        # Convert to seconds and sleep
        sleep(delay / 1000)

    def _should_retry(self, error: Optional[ApiError], request: Request) -> bool:
        """
        Determine whether the request should be retried based on status code and HTTP method.
        By default, retries all 5xx server errors and specific 4xx client errors (408 Timeout, 429 Rate Limit).
        Per-request retry config overrides SDK defaults for status codes and HTTP methods.

        :param Optional[ApiError] error: The error from the previous handler.
        :param Request request: The request being retried.
        :return: True if the request should be retried, False otherwise.
        :rtype: bool
        """
        if not error:
            return False

        retry_config = (request.config or {}).get("retry") or {}

        # Check if status code is retryable
        request_status_codes = retry_config.get("status_codes_to_retry")
        if request_status_codes is not None:
            should_retry_status = error.status in request_status_codes
        elif self._status_codes_to_retry is not None:
            should_retry_status = error.status in self._status_codes_to_retry
        else:
            # Default: retry 5xx, 408 (Timeout), 429 (Rate Limit)
            should_retry_status = (
                error.status >= 500 or error.status == 408 or error.status == 429
            )

        # Check if HTTP method is retryable
        request_http_methods = retry_config.get("http_methods_to_retry")
        if request_http_methods is not None:
            should_retry_method = request.method.upper() in {
                m.upper() for m in request_http_methods
            }
        else:
            should_retry_method = request.method.upper() in self._http_methods_to_retry

        return should_retry_status and should_retry_method
