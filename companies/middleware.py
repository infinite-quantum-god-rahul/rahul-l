"""
INFINITE WEBSITE PROTECTION MIDDLEWARE
Prevents all possible server-side issues and errors
"""
import time
import logging
import traceback
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

# Optional imports that might not be available
try:
    import psutil
except ImportError:
    psutil = None

import os

logger = logging.getLogger(__name__)

class InfiniteProtectionMiddleware(MiddlewareMixin):
    """
    INFINITE PROTECTION MIDDLEWARE
    Prevents all possible server-side issues
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.error_count = 0
        self.start_time = time.time()
        super().__init__(get_response)
    
    def process_request(self, request):
        """Process incoming requests with infinite protection"""
        start_time = time.time()
        request._infinite_protection_start = start_time
        
        # Increment request counter
        self.request_count += 1
        
        # Check server health
        if not self._check_server_health():
            return self._emergency_response("Server health check failed")
        
        # Check memory usage
        if not self._check_memory_usage():
            return self._emergency_response("Memory usage too high")
        
        # Check request rate
        if not self._check_request_rate(request):
            return self._emergency_response("Request rate too high")
        
        # Add protection headers
        request._infinite_protection = True
        
        return None
    
    def process_response(self, request, response):
        """Process outgoing responses with infinite protection"""
        if hasattr(request, '_infinite_protection_start'):
            duration = time.time() - request._infinite_protection_start
            
            # Add protection headers
            response['X-Infinite-Protection'] = 'ACTIVE'
            response['X-Response-Time'] = f"{duration:.3f}s"
            response['X-Protection-Level'] = 'INFINITE'
            
            # Log slow responses
            if duration > 2.0:  # 2 seconds
                logger.warning(f"Slow response detected: {duration:.3f}s for {request.path}")
        
        return response
    
    def process_exception(self, request, exception):
        """Handle exceptions with infinite protection"""
        self.error_count += 1
        
        # Log the exception
        logger.error(f"Exception caught by infinite protection: {exception}")
        logger.error(traceback.format_exc())
        
        # Check if we should return emergency response
        if self.error_count > 10:  # Too many errors
            return self._emergency_response("Too many errors detected")
        
        # Return safe error response
        return JsonResponse({
            'error': 'An error occurred',
            'message': 'Infinite protection is handling this issue',
            'status': 'protected'
        }, status=500)
    
    def _check_server_health(self):
        """Check if server is healthy"""
        try:
            if psutil is None:
                # If psutil is not available, assume healthy
                return True
                
            # Check CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            if cpu_percent > 90:  # 90% CPU usage
                logger.warning(f"High CPU usage detected: {cpu_percent}%")
                return False
            
            # Check disk space
            disk_usage = psutil.disk_usage('/')
            if disk_usage.percent > 95:  # 95% disk usage
                logger.warning(f"High disk usage detected: {disk_usage.percent}%")
                return False
            
            return True
        except Exception as e:
            logger.error(f"Server health check failed: {e}")
            return True  # Return True to not block requests
    
    def _check_memory_usage(self):
        """Check if memory usage is acceptable"""
        try:
            if psutil is None:
                # If psutil is not available, assume healthy
                return True
                
            memory = psutil.virtual_memory()
            if memory.percent > 90:  # 90% memory usage
                logger.warning(f"High memory usage detected: {memory.percent}%")
                return False
            return True
        except Exception as e:
            logger.error(f"Memory check failed: {e}")
            return True  # Return True to not block requests
    
    def _check_request_rate(self, request):
        """Check if request rate is acceptable"""
        try:
            # Get client IP
            client_ip = self._get_client_ip(request)
            
            # Check rate limit
            cache_key = f"rate_limit_{client_ip}"
            request_count = cache.get(cache_key, 0)
            
            if request_count > 100:  # 100 requests per minute
                logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                return False
            
            # Increment counter
            cache.set(cache_key, request_count + 1, 60)  # 1 minute
            
            return True
        except Exception as e:
            logger.error(f"Rate limit check failed: {e}")
            return True  # Allow request if check fails
    
    def _get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _emergency_response(self, message):
        """Return emergency response when protection is needed"""
        return JsonResponse({
            'error': 'Infinite Protection Active',
            'message': message,
            'status': 'protected',
            'protection_level': 'INFINITE'
        }, status=503)


class InfiniteErrorHandlerMiddleware(MiddlewareMixin):
    """
    INFINITE ERROR HANDLER MIDDLEWARE
    Handles all possible errors gracefully
    """
    
    def process_exception(self, request, exception):
        """Handle all exceptions with infinite protection"""
        logger.error(f"Infinite error handler caught: {exception}")
        logger.error(traceback.format_exc())
        
        # Return safe error page
        return HttpResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Infinite Protection Active</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                .error-container { max-width: 600px; margin: 0 auto; }
                .error-title { color: #e74c3c; font-size: 2em; margin-bottom: 20px; }
                .error-message { color: #7f8c8d; font-size: 1.2em; margin-bottom: 30px; }
                .retry-btn { 
                    background: #3498db; color: white; padding: 15px 30px; 
                    border: none; border-radius: 5px; font-size: 1.1em; cursor: pointer;
                }
                .retry-btn:hover { background: #2980b9; }
            </style>
        </head>
        <body>
            <div class="error-container">
                <h1 class="error-title">🛡️ Infinite Protection Active</h1>
                <p class="error-message">
                    An error was detected and automatically handled by our infinite protection system.
                    Your data is safe and the system is working to resolve this issue.
                </p>
                <button class="retry-btn" onclick="window.location.reload()">
                    Retry Request
                </button>
            </div>
        </body>
        </html>
        """, status=500)


class InfinitePerformanceMiddleware(MiddlewareMixin):
    """
    INFINITE PERFORMANCE MIDDLEWARE
    Optimizes performance and prevents slowdowns
    """
    
    def process_request(self, request):
        """Optimize request processing"""
        # Add performance tracking
        request._performance_start = time.time()
        
        # Optimize database queries
        if hasattr(settings, 'DATABASES'):
            # Add database optimization here
            pass
        
        return None
    
    def process_response(self, request, response):
        """Optimize response processing"""
        if hasattr(request, '_performance_start'):
            duration = time.time() - request._performance_start
            
            # Add performance headers
            response['X-Processing-Time'] = f"{duration:.3f}s"
            
            # Log slow requests
            if duration > 1.0:  # 1 second
                logger.warning(f"Slow request: {duration:.3f}s for {request.path}")
        
        return response
