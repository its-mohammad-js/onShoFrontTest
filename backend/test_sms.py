#!/usr/bin/env python
"""
Test script for SMS functionality
"""

import os
import sys
import django

# Add the project directory to the path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mahoverse.settings')
django.setup()

from account.sms_service import SMSService
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_sms_service():
    """Test the SMS service functionality"""
    
    print("🧪 Testing SMS Service...")
    print("=" * 50)
    
    # Initialize SMS service
    sms_service = SMSService()
    
    # Test 1: Phone number validation
    print("\n1️⃣ Testing phone number validation...")
    test_numbers = [
        "+989360444045",  # Valid international
        "09360444045",    # Valid Iranian
        "9360444045",     # Valid Iranian without leading 0
        "invalid_number", # Invalid
        "",               # Empty
    ]
    
    for number in test_numbers:
        is_valid = sms_service._validate_phone_number(number)
        normalized = sms_service._normalize_phone_number(number)
        print(f"   {number} -> Valid: {is_valid}, Normalized: {normalized}")
    
    # Test 2: Input validation
    print("\n2️⃣ Testing input validation...")
    
    # Test with empty recipients
    result = sms_service.send_sms([], "Test message")
    print(f"   Empty recipients: {result['status']} - {result.get('error', 'No error')}")
    
    # Test with empty message
    result = sms_service.send_sms(["+989120000000"], "")
    print(f"   Empty message: {result['status']} - {result.get('error', 'No error')}")
    
    # Test 3: OTP SMS (without actually sending)
    print("\n3️⃣ Testing OTP SMS preparation...")
    result = sms_service.send_otp_sms("09120000000", "123456")
    if result['status']:
        print("   ✅ OTP SMS prepared successfully")
        print(f"   Message: {result.get('message', 'No message')}")
    else:
        print(f"   ❌ OTP SMS preparation failed: {result.get('error', 'Unknown error')}")
    
    # Test 4: Welcome SMS (without actually sending)
    print("\n4️⃣ Testing Welcome SMS preparation...")
    result = sms_service.send_welcome_sms("09120000000", "علی")
    if result['status']:
        print("   ✅ Welcome SMS prepared successfully")
        print(f"   Message: {result.get('message', 'No message')}")
    else:
        print(f"   ❌ Welcome SMS preparation failed: {result.get('error', 'Unknown error')}")
    
    # Test 5: Actual SMS sending (commented out by default)
    print("\n5️⃣ Testing actual SMS sending...")
    print("   ⚠️  This will actually send SMS messages and use your API credits!")
    user_input = input("   Do you want to send a test SMS? (y/N): ").strip().lower()
    
    if user_input == 'y':
        phone_number = input("   Enter phone number (e.g., 09120000000): ").strip()
        test_message = input("   Enter test message: ").strip()
        
        if phone_number and test_message:
            print("   Sending SMS...")
            result = sms_service.send_sms([phone_number], test_message)
            
            if result['status']:
                print("   ✅ SMS sent successfully!")
                print(f"   Response: {result.get('data', {})}")
            else:
                print(f"   ❌ SMS sending failed: {result.get('error', 'Unknown error')}")
                print(f"   Full response: {result}")
        else:
            print("   ❌ Phone number or message is empty")
    else:
        print("   Skipping actual SMS sending test")
    
    print("\n" + "=" * 50)
    print("✅ SMS Service testing completed!")

if __name__ == "__main__":
    try:
        test_sms_service()
    except KeyboardInterrupt:
        print("\n\n❌ Testing interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Testing failed with error: {str(e)}")
        logger.exception("Test failed with exception")