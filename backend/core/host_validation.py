"""
Middleware to validate dynamic subdomains for onsho24.ir
This middleware validates hosts before they reach Django's ALLOWED_HOSTS check
"""
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest, HttpResponseBadRequest
from django.conf import settings


class DynamicSubdomainHostMiddleware(MiddlewareMixin):
    """
    Middleware to validate and allow any subdomain of onsho24.ir
    This runs early in the middleware stack to validate hosts
    """
    
    ALLOWED_DOMAINS = [
        'onsho24.ir',
        'www.onsho24.ir',
    ]
    
    RESERVED_SUBDOMAINS = ['www', 'api', 'admin', 'mail', 'ftp', 'cpanel']
    
    def process_request(self, request: HttpRequest):
        host = request.get_host().lower()
        
        # Remove port if present (e.g., "localhost:8000" -> "localhost")
        if ':' in host:
            host = host.split(':')[0]
        
        # Allow localhost and 127.0.0.1 for development
        if host in ['localhost', '127.0.0.1', 'testserver']:
            return None
        
        # Allow exact matches for main domains
        if host in self.ALLOWED_DOMAINS:
            return None
        
        # Check if it's a subdomain of onsho24.ir
        if host.endswith('.onsho24.ir'):
            subdomain = host.replace('.onsho24.ir', '').lower()
            
            # Block reserved subdomains
            if subdomain in self.RESERVED_SUBDOMAINS:
                return HttpResponseBadRequest(f"Subdomain '{subdomain}' is reserved and cannot be used.")
            
            # Allow any other subdomain - store original host for later use
            request.META['HTTP_X_ORIGINAL_HOST'] = request.META.get('HTTP_HOST', host)
            return None
        
        # For all other hosts in production, validate against ALLOWED_HOSTS
        # In DEBUG mode, we allow all hosts
        if not settings.DEBUG:
            from django.http import HttpResponseForbidden
            if host not in settings.ALLOWED_HOSTS:
                return HttpResponseForbidden(f"Invalid HTTP_HOST header: '{host}'. You may need to add '{host}' to ALLOWED_HOSTS.")
        
        return None

