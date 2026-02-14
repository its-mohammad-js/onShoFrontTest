"""
Custom pipeline for social auth to handle user creation/retrieval
"""
from django.contrib.auth import get_user_model
from django.utils import timezone
from social_core.pipeline.user import get_username as social_get_username
from social_core.exceptions import AuthException

User = get_user_model()


def get_user_by_email(strategy, details, backend, user=None, *args, **kwargs):
    """
    Get user by email if exists, otherwise create new user
    """
    if user:
        return {'user': user}
    
    email = details.get('email')
    if not email:
        raise AuthException(backend, 'Email is required for Google authentication')
    
    # Try to find user by email
    try:
        user = User.objects.get(email=email)
        return {
            'is_new': False,
            'user': user
        }
    except User.DoesNotExist:
        # Create new user
        # Generate a unique phone number if not provided
        # For Google OAuth users, we'll use email-based phone number
        phone_number = f"09{email[:9].replace('@', '').replace('.', '')[:9]}"
        
        # Ensure phone number is unique
        counter = 1
        original_phone = phone_number
        while User.objects.filter(phone_number=phone_number).exists():
            phone_number = f"{original_phone[:-1]}{counter}"
            counter += 1
            if counter > 99:
                # Fallback: use timestamp
                import time
                phone_number = f"09{str(int(time.time()))[-9:]}"
                break
        
        # Get default role (دانشجو)
        from account.models import Role
        try:
            role = Role.objects.get(slug='دانشجو')
        except Role.DoesNotExist:
            role = None
        
        user = User.objects.create_user(
            phone_number=phone_number,
            email=email,
            first_name=details.get('first_name', ''),
            last_name=details.get('last_name', ''),
            role=role,
            email_verified_date=timezone.now() if hasattr(timezone, 'now') else None,
            is_verified=True,  # Google verified email
        )
        
        return {
            'is_new': True,
            'user': user
        }

