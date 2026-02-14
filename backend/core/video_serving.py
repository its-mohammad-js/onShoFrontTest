"""
View برای سرو ویدیوها با پشتیبانی از CORS headers و Range requests
این view خطای ERR_BLOCKED_BY_ORB را برطرف می‌کند
"""
import os
import re
from django.http import FileResponse, HttpResponse, Http404
from django.conf import settings
from pathlib import Path


def get_content_type(file_path):
    """
    تشخیص Content-Type بر اساس extension فایل
    """
    ext = Path(file_path).suffix.lower()
    content_types = {
        '.mp4': 'video/mp4',
        '.webm': 'video/webm',
        '.ogg': 'video/ogg',
        '.ogv': 'video/ogg',
        '.mov': 'video/quicktime',
        '.avi': 'video/x-msvideo',
    }
    return content_types.get(ext, 'application/octet-stream')


def serve_video(request, file_path):
    """
    سرو ویدیو با پشتیبانی از CORS headers و Range requests
    
    Args:
        request: Django request object
        file_path: مسیر نسبی فایل ویدیو از MEDIA_ROOT
    
    Returns:
        FileResponse با headers مناسب برای CORS و Range requests
    """
    # ساخت مسیر کامل فایل
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    
    # بررسی وجود فایل
    if not os.path.exists(full_path):
        raise Http404("Video file not found")
    
    # بررسی اینکه فایل در MEDIA_ROOT است (امنیت)
    full_path = os.path.abspath(full_path)
    media_root = os.path.abspath(settings.MEDIA_ROOT)
    if not full_path.startswith(media_root):
        raise Http404("Invalid file path")
    
    # تشخیص Content-Type
    content_type = get_content_type(full_path)
    
    # خواندن اندازه فایل
    file_size = os.path.getsize(full_path)
    
    # بررسی Range request
    range_header = request.META.get('HTTP_RANGE', '').strip()
    
    # Headers پایه برای CORS
    # استفاده از VIDEO_CORS_ORIGIN از settings یا '*' به صورت پیش‌فرض
    cors_origin = getattr(settings, 'VIDEO_CORS_ORIGIN', '*')
    headers = {
        'Access-Control-Allow-Origin': cors_origin,
        'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
        'Access-Control-Allow-Headers': 'Range',
        'Access-Control-Expose-Headers': 'Content-Range, Content-Length, Accept-Ranges',
        'Accept-Ranges': 'bytes',
        'Content-Type': content_type,
    }
    
    # اگر OPTIONS request است (preflight)
    if request.method == 'OPTIONS':
        response = HttpResponse(status=200)
        for key, value in headers.items():
            response[key] = value
        return response
    
    # اگر HEAD request است
    if request.method == 'HEAD':
        response = HttpResponse(status=200)
        response['Content-Length'] = str(file_size)
        for key, value in headers.items():
            response[key] = value
        return response
    
    # پردازش Range request
    if range_header:
        # Parse Range header: bytes=start-end
        range_match = re.match(r'bytes=(\d*)-(\d*)', range_header)
        
        if range_match:
            start_str = range_match.group(1)
            end_str = range_match.group(2)
            
            # محاسبه start و end
            if start_str:
                start = int(start_str)
            else:
                start = 0
            
            if end_str:
                end = int(end_str)
            else:
                end = file_size - 1
            
            # اعتبارسنجی range
            if start >= file_size or end >= file_size or start > end:
                response = HttpResponse(status=416)  # Range Not Satisfiable
                response['Content-Range'] = f'bytes */{file_size}'
                for key, value in headers.items():
                    response[key] = value
                return response
            
            # تنظیم headers برای partial content
            content_length = end - start + 1
            headers['Content-Range'] = f'bytes {start}-{end}/{file_size}'
            headers['Content-Length'] = str(content_length)
            
            # باز کردن فایل و خواندن range
            with open(full_path, 'rb') as video_file:
                video_file.seek(start)
                content = video_file.read(content_length)
            
            response = HttpResponse(content, status=206)  # Partial Content
            for key, value in headers.items():
                response[key] = value
            
            return response
    
    # اگر Range request نبود، کل فایل را برگردان
    video_file = open(full_path, 'rb')
    response = FileResponse(video_file, content_type=content_type)
    
    # اضافه کردن headers
    for key, value in headers.items():
        response[key] = value
    
    response['Content-Length'] = str(file_size)
    
    return response

