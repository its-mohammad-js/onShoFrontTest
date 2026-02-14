"""
Middleware برای اضافه کردن CORS headers به فایل‌های media
این middleware خطای ERR_BLOCKED_BY_ORB را برطرف می‌کند
"""
from django.http import HttpResponse, StreamingHttpResponse, FileResponse
from django.conf import settings
from pathlib import Path


class MediaCorsMiddleware:
    """
    Middleware برای اضافه کردن CORS headers به فایل‌های media
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # بررسی اینکه آیا این یک فایل media است
        # حذف query parameters از path
        path = request.path.lower().split('?')[0]
        media_extensions = ['.mp4', '.webm', '.ogg', '.ogv', '.mov', '.avi', 
                          '.mp3', '.wav', '.flac', '.aac', '.m4a',
                          '.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
        
        is_media_file = any(path.endswith(ext) for ext in media_extensions)
        
        # بررسی اینکه آیا مسیر media است یا video-proxy
        is_media_path = (path.startswith('/api/media/') or 
                        path.startswith('/media/') or
                        'video-proxy' in path or
                        'video_proxy' in path)
        
        # اگر Content-Type header نشان می‌دهد که این یک media file است
        content_type_header = response.get('Content-Type', '') or ''
        if isinstance(content_type_header, list):
            content_type_header = content_type_header[0] if content_type_header else ''
        content_type = str(content_type_header).lower()
        is_media_by_content_type = any(ct in content_type for ct in [
            'video/', 'audio/', 'image/'
        ])
        
        # اگر video-proxy endpoint است یا media file است
        is_video_proxy = 'video-proxy' in path or 'video_proxy' in path
        
        if is_video_proxy or (is_media_file and is_media_path) or (is_media_by_content_type and is_media_path):
            # دریافت CORS origin از settings
            cors_origin = getattr(settings, 'VIDEO_CORS_ORIGIN', '*')
            
            # اضافه کردن CORS headers
            # استفاده از setdefault برای جلوگیری از overwrite کردن headers موجود
            if 'Access-Control-Allow-Origin' not in response:
                response['Access-Control-Allow-Origin'] = cors_origin
            if 'Access-Control-Allow-Methods' not in response:
                response['Access-Control-Allow-Methods'] = 'GET, HEAD, OPTIONS'
            if 'Access-Control-Allow-Headers' not in response:
                response['Access-Control-Allow-Headers'] = 'Range'
            if 'Access-Control-Expose-Headers' not in response:
                response['Access-Control-Expose-Headers'] = 'Content-Range, Content-Length, Accept-Ranges'
            if 'Accept-Ranges' not in response:
                response['Accept-Ranges'] = 'bytes'
            
            # اگر Content-Type تنظیم نشده، بر اساس extension تنظیم کن
            if 'Content-Type' not in response:
                ext = Path(path).suffix.lower()
                content_types = {
                    '.mp4': 'video/mp4',
                    '.webm': 'video/webm',
                    '.ogg': 'video/ogg',
                    '.ogv': 'video/ogg',
                    '.mov': 'video/quicktime',
                    '.avi': 'video/x-msvideo',
                    '.mp3': 'audio/mpeg',
                    '.wav': 'audio/wav',
                    '.flac': 'audio/flac',
                    '.aac': 'audio/aac',
                    '.m4a': 'audio/mp4',
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.png': 'image/png',
                    '.gif': 'image/gif',
                    '.webp': 'image/webp',
                    '.svg': 'image/svg+xml',
                }
                if ext in content_types:
                    response['Content-Type'] = content_types[ext]
        
        return response

