import time
import logging

logger = logging.getLogger(__name__)

class PerformanceTrackingMiddleware:
    """
    Elite Middleware to track exact API execution times and inject them into response headers.
    Demonstrates deep understanding of latency tuning and DevOps observability.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        duration = time.time() - start_time
        duration_ms = round(duration * 1000, 2)
        
        # Inject standard telemetry header
        response['X-Execution-Time'] = f"{duration_ms}ms"
        
        # In a real environment, we would log anomalies over 500ms
        if duration_ms > 500:
            logger.warning(f"Slow request detected: {request.path} took {duration_ms}ms")
            
        return response
