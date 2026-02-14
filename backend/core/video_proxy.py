"""
Video Proxy View برای proxy کردن ویدیوهای خارجی (مثل Aparat)
با پشتیبانی از CORS headers و Range requests
"""
import requests
import re
from django.http import HttpResponse, StreamingHttpResponse, Http404
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class VideoProxyView(APIView):
    """
    Proxy view برای ویدیوهای خارجی با CORS headers
    """
    
    def get(self, request):
        """
        Proxy کردن ویدیو از URL خارجی
        Query parameter: url - URL ویدیو برای proxy کردن
        """
        video_url = request.GET.get('url')
        
        if not video_url:
            return Response(
                {'error': 'URL parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # دریافت CORS origin از settings
            cors_origin = getattr(settings, 'VIDEO_CORS_ORIGIN', '*')
            
            # دریافت Range header از request
            range_header = request.META.get('HTTP_RANGE', '').strip()
            
            # تنظیم headers برای request به سرور خارجی
            headers = {
                'User-Agent': request.META.get('HTTP_USER_AGENT', 'Mozilla/5.0'),
                'Referer': video_url,
            }
            
            if range_header:
                headers['Range'] = range_header
            
            # درخواست به سرور خارجی
            response = requests.get(
                video_url,
                headers=headers,
                stream=True,
                timeout=30
            )
            
            # بررسی status code
            if response.status_code not in [200, 206]:
                return Response(
                    {'error': f'Failed to fetch video: {response.status_code}'},
                    status=status.HTTP_502_BAD_GATEWAY
                )
            
            # تنظیم CORS headers
            cors_headers = {
                'Access-Control-Allow-Origin': cors_origin,
                'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
                'Access-Control-Allow-Headers': 'Range',
                'Access-Control-Expose-Headers': 'Content-Range, Content-Length, Accept-Ranges',
                'Accept-Ranges': 'bytes',
            }
            
            # کپی کردن headers مهم از response اصلی
            content_type = response.headers.get('Content-Type', 'video/mp4')
            content_length = response.headers.get('Content-Length')
            content_range = response.headers.get('Content-Range')
            accept_ranges = response.headers.get('Accept-Ranges', 'bytes')
            
            # اگر Range request بود و 206 Partial Content برگشت
            if response.status_code == 206:
                # استفاده از StreamingHttpResponse برای partial content
                django_response = StreamingHttpResponse(
                    response.iter_content(chunk_size=8192),
                    status=206
                )
                
                # تنظیم headers
                django_response['Content-Type'] = content_type
                if content_length:
                    django_response['Content-Length'] = content_length
                if content_range:
                    django_response['Content-Range'] = content_range
                django_response['Accept-Ranges'] = accept_ranges
                
                # اضافه کردن CORS headers
                for key, value in cors_headers.items():
                    django_response[key] = value
                
                return django_response
            else:
                # برای full content
                django_response = StreamingHttpResponse(
                    response.iter_content(chunk_size=8192),
                    status=200
                )
                
                django_response['Content-Type'] = content_type
                if content_length:
                    django_response['Content-Length'] = content_length
                django_response['Accept-Ranges'] = accept_ranges
                
                # اضافه کردن CORS headers
                for key, value in cors_headers.items():
                    django_response[key] = value
                
                return django_response
                
        except requests.exceptions.RequestException as e:
            return Response(
                {'error': f'Failed to proxy video: {str(e)}'},
                status=status.HTTP_502_BAD_GATEWAY
            )
        except Exception as e:
            return Response(
                {'error': f'Internal server error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def options(self, request):
        """
        Handle OPTIONS request (CORS preflight)
        """
        cors_origin = getattr(settings, 'VIDEO_CORS_ORIGIN', '*')
        response = HttpResponse(status=200)
        response['Access-Control-Allow-Origin'] = cors_origin
        response['Access-Control-Allow-Methods'] = 'GET, HEAD, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Range'
        response['Access-Control-Expose-Headers'] = 'Content-Range, Content-Length, Accept-Ranges'
        return response
    
    def head(self, request):
        """
        Handle HEAD request
        """
        video_url = request.GET.get('url')
        if not video_url:
            return HttpResponse(status=400)
        
        try:
            response = requests.head(video_url, timeout=10)
            cors_origin = getattr(settings, 'VIDEO_CORS_ORIGIN', '*')
            
            django_response = HttpResponse(status=response.status_code)
            django_response['Access-Control-Allow-Origin'] = cors_origin
            django_response['Access-Control-Allow-Methods'] = 'GET, HEAD, OPTIONS'
            django_response['Access-Control-Allow-Headers'] = 'Range'
            django_response['Access-Control-Expose-Headers'] = 'Content-Range, Content-Length, Accept-Ranges'
            
            if 'Content-Length' in response.headers:
                django_response['Content-Length'] = response.headers['Content-Length']
            if 'Content-Type' in response.headers:
                django_response['Content-Type'] = response.headers['Content-Type']
            if 'Accept-Ranges' in response.headers:
                django_response['Accept-Ranges'] = response.headers['Accept-Ranges']
            
            return django_response
        except Exception as e:
            return HttpResponse(status=502)

