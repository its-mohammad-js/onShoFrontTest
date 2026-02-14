from django.urls import path
from . import views

# app_name removed to avoid namespace conflict when included multiple times
# Namespace will be defined in main urls.py if needed
urlpatterns = [
    path('login', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('init', views.UserProfileView.as_view(), name='profile'),
    path('edit', views.UserProfileEditView.as_view(), name='profile_edit'),
    path('code/send', views.SendOTPCodeView.as_view(), name='send_otp'),
    path('code/check', views.CheckOTPCodeView.as_view(), name='verify_otp'),
    path('register', views.UserRegisterView.as_view(), name='register'),
    path('organization', views.OrganizationRegisterView.as_view(), name='organization_register'),
    path('password', views.ChangePasswordView.as_view(), name='change_password'),
    path('permissions/list', views.PermissionListAPIView.as_view(), name='permission-list'),
    path('permissions/user', views.UserRolePermissionListAPIView.as_view(), name='user-permissions'),
    path('manual-user/create', views.ManualUserCreateView.as_view(), name='manual-user-create'),
    path('google/login', views.GoogleLoginView.as_view(), name='google-login'),
    path('google/callback', views.GoogleCallbackView.as_view(), name='google-callback'),
]
