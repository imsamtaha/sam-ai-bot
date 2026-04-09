import time
import logging
import threading
from collections import defaultdict, deque
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Maximum number of response-time samples kept per endpoint (sliding window)
_MAX_RESPONSE_SAMPLES = 1000

# Decimal places used when rounding the error rate
_ERROR_RATE_PRECISION = 4

# Lock protecting concurrent access to _metrics
_lock = threading.Lock()

# In-memory metrics storage
_metrics: Dict[str, Any] = {
    'request_counts': defaultdict(int),
    'error_counts': defaultdict(int),
    'response_times': defaultdict(lambda: deque(maxlen=_MAX_RESPONSE_SAMPLES)),
    'total_requests': 0,
    'total_errors': 0,
    'start_time': time.time(),
}


def record_request(endpoint: str) -> None:
    """Record an incoming request for the given endpoint."""
    with _lock:
        _metrics['request_counts'][endpoint] += 1
        _metrics['total_requests'] += 1


def record_error(endpoint: str) -> None:
    """Record an error for the given endpoint."""
    with _lock:
        _metrics['error_counts'][endpoint] += 1
        _metrics['total_errors'] += 1


def record_response_time(endpoint: str, duration_seconds: float) -> None:
    """Record a response time (in seconds) for the given endpoint."""
    with _lock:
        _metrics['response_times'][endpoint].append(duration_seconds)


def get_metrics() -> Dict[str, Any]:
    """Return a snapshot of current performance metrics."""
    with _lock:
        uptime = time.time() - _metrics['start_time']
        total_requests = _metrics['total_requests']
        total_errors = _metrics['total_errors']

        per_endpoint = {}
        all_endpoints = set(
            list(_metrics['request_counts'].keys()) +
            list(_metrics['response_times'].keys())
        )
        for endpoint in all_endpoints:
            times = list(_metrics['response_times'].get(endpoint, []))
            avg_ms = (sum(times) / len(times) * 1000) if times else None
            min_ms = (min(times) * 1000) if times else None
            max_ms = (max(times) * 1000) if times else None
            per_endpoint[endpoint] = {
                'request_count': _metrics['request_counts'].get(endpoint, 0),
                'error_count': _metrics['error_counts'].get(endpoint, 0),
                'avg_response_time_ms': round(avg_ms, 2) if avg_ms is not None else None,
                'min_response_time_ms': round(min_ms, 2) if min_ms is not None else None,
                'max_response_time_ms': round(max_ms, 2) if max_ms is not None else None,
            }

        return {
            'uptime_seconds': round(uptime, 2),
            'total_requests': total_requests,
            'total_errors': total_errors,
            'error_rate': round(
                total_errors / total_requests, _ERROR_RATE_PRECISION
            ) if total_requests > 0 else 0.0,
            'endpoints': per_endpoint,
        }
