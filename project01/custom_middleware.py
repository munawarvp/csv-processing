from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
import time


class RateLimitMiddleware(MiddlewareMixin):
    REQUEST_LIMIT = 100  # Maximum number of requests allowed
    TIME_LIMIT = 300    # Time window in seconds (5 minutes)

    def _get_client_ip(self, request):
        """Retrieve the client's IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _get_cache_key(self, ip):
        """Generate a unique cache key for the IP address."""
        return f"rate_limit:{ip}"

    def process_request(self, request):
        """Check if the IP address exceeds the rate limit."""
        ip = self._get_client_ip(request)
        cache_key = self._get_cache_key(ip)

        # Get the current timestamp
        current_time = time.time()

        # Retrieve request timestamps from the cache
        request_timestamps = cache.get(cache_key, [])

        # Filter out timestamps that are outside the time window
        valid_timestamps = [ts for ts in request_timestamps if current_time - ts <= self.TIME_LIMIT]

        # Check if the number of requests exceeds the limit
        if len(valid_timestamps) >= self.REQUEST_LIMIT:
            retry_after = self.TIME_LIMIT - (current_time - valid_timestamps[0])
            return JsonResponse(
                {
                    "error": "Too Many Requests",
                    "message": f"Rate limit exceeded. Try again in {int(retry_after)} seconds."
                },
                status=429,
            )

        # Add the current timestamp to the list
        valid_timestamps.append(current_time)

        # Update the cache with the new list of timestamps
        cache.set(cache_key, valid_timestamps, timeout=self.TIME_LIMIT)

        # Add headers to indicate remaining allowed requests
        remaining_requests = self.REQUEST_LIMIT - len(valid_timestamps)
        request.META["HTTP_X_RATE_LIMIT_REMAINING"] = remaining_requests

    def process_response(self, request, response):
        """Include rate limit headers in the response."""
        remaining_requests = request.META.get("HTTP_X_RATE_LIMIT_REMAINING")
        if remaining_requests is not None:
            response["X-RateLimit-Limit"] = self.REQUEST_LIMIT
            response["X-RateLimit-Remaining"] = remaining_requests
        return response
        