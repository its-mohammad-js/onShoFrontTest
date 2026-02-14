from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            # فراخوانی متد اصلی احراز هویت
            return super().authenticate(request)
        except InvalidToken as e:
            # مدیریت خطای توکن نامعتبر
            raise AuthenticationFailed({
                "status": False,
                "data": {
                    "error": "توکن داده شده معتبر نیست یا منقضی شده است."
                }
            })
        except TokenError as e:
            # مدیریت سایر خطاهای مرتبط با توکن
            raise AuthenticationFailed({
                "status": False,
                "data": {
                    "error": "مشکلی در احراز هویت توکن وجود دارد."
                }
            })
        except Exception as e:
            # مدیریت خطاهای غیرمنتظره
            raise AuthenticationFailed({
                "status": False,
                "data": {
                    "error": "یک خطای غیرمنتظره در احراز هویت رخ داده است."
                }
            })
