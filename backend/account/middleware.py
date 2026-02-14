"""
Middleware برای بررسی subdomain و پیدا کردن organizer مرتبط
"""
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin
from django.db.models import Q
from .models import Organizer


class SubdomainOrganizerMiddleware(MiddlewareMixin):
    """
    این middleware subdomain را از Host header استخراج می‌کند
    و organizer مرتبط را پیدا می‌کند
    """
    
    def process_request(self, request):
        # دریافت Host header
        host = request.get_host()
        
        # نادیده گرفتن برای دامنه اصلی (onsho24.ir, www.onsho24.ir)
        if host in ['onsho24.ir', 'www.onsho24.ir'] or host.startswith('localhost') or host.startswith('127.0.0.1'):
            request.organizer = None
            return None
        
        # استخراج subdomain
        # مثال: sazman.onsho24.ir -> sazman
        parts = host.split('.')
        if len(parts) >= 3:
            subdomain = parts[0].lower()
            
            # نادیده گرفتن subdomain های خاص
            if subdomain in ['www', 'api', 'admin', 'mail', 'ftp', 'cpanel']:
                request.organizer = None
                return None
            
            # جستجوی organizer بر اساس subdomain
            try:
                # جستجو بر اساس subdomain field
                # subdomain فقط نام subdomain را ذخیره می‌کند (مثال: "sazman")
                organizer = Organizer.objects.filter(
                    subdomain__iexact=subdomain,
                    is_active=True,
                    is_verified=True
                ).first()
                
                if organizer:
                    request.organizer = organizer
                    request.subdomain = subdomain
                else:
                    raise Organizer.DoesNotExist
            except Organizer.DoesNotExist:
                # اگر organizer پیدا نشد، 404 برگردان
                # فقط برای مسیرهای خاص مثل admin، API و static files، 404 نده
                path = request.path
                excluded_paths = ['/admin/', '/auth/', '/static/', '/media/', '/api/', 
                                '/course/', '/payment/', '/ticket/', '/webinar/', 
                                '/static-content/', '/social-auth/']
                if any(path.startswith(excluded) for excluded in excluded_paths):
                    request.organizer = None
                    request.subdomain = None
                    return None
                # برای همه مسیرهای دیگر (از جمله root path) 404 برگردان
                raise Http404("Organizer not found for this subdomain")
        else:
            request.organizer = None
            request.subdomain = None
        
        return None

