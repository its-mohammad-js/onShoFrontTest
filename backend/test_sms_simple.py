#!/usr/bin/env python
"""
Simple test script for SMS functionality without Django dependencies
"""

import sys
import os

# Add the project directory to the path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Mock Django settings for testing
class MockSettings:
    DEBUG = True

sys.modules['django.conf'] = type(sys)('django.conf')
sys.modules['django.conf'].settings = MockSettings()

import requests
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SMSService:
    """
    SMS Service for sending SMS messages using the provided API
    """
    
    def __init__(self):
        self.api_key = "YTA0NjhjZmEtYjEzOC00YTNlLWFiY2QtYmZiZTMwYTEyMDQ5YTgzYjk2MmNmZjkzMzE3NzRkNWJlNDUzNzgxY2E1MjE="
        self.base_url = "https://api.sms.ir"
        self.from_number = "+983000505"
        self.timeout = 30
        self.max_retries = 3
        
    def _make_request(self, method, endpoint, headers=None, json_data=None, retries=0):
        """Make HTTP request with retry logic and proper error handling"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            logger.info(f"Making {method} request to {url}")
            
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=json_data,
                timeout=self.timeout
            )
            
            logger.info(f"Response status: {response.status_code}")
            
            try:
                response_data = response.json()
            except ValueError:
                response_data = {"message": response.text}
            
            if response.status_code == 200:
                logger.info(f"Request successful: {response_data}")
                return {'status': True, 'data': response_data}
            else:
                logger.error(f"Request failed with status {response.status_code}: {response_data}")
                return {
                    'status': False,
                    'error': f"HTTP {response.status_code}: {response_data.get('message', 'Unknown error')}",
                    'data': response_data
                }
                
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout for {url}")
            if retries < self.max_retries:
                logger.info(f"Retrying request (attempt {retries + 1}/{self.max_retries})")
                return self._make_request(method, endpoint, headers, json_data, retries + 1)
            return {'status': False, 'error': 'Request timeout - please try again later'}
            
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error for {url}: {str(e)}")
            if retries < self.max_retries:
                logger.info(f"Retrying request (attempt {retries + 1}/{self.max_retries})")
                return self._make_request(method, endpoint, headers, json_data, retries + 1)
            return {'status': False, 'error': 'Connection error - please check your internet connection'}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for {url}: {str(e)}")
            return {'status': False, 'error': f'Request failed: {str(e)}'}
            
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {str(e)}")
            return {'status': False, 'error': f'Unexpected error: {str(e)}'}
    
    def _validate_phone_number(self, phone_number):
        """Validate phone number format"""
        if not phone_number or not isinstance(phone_number, str):
            return False
            
        phone_number = phone_number.strip()
        
        if phone_number.startswith('+'):
            return len(phone_number) >= 11 and len(phone_number) <= 15
        
        if phone_number.startswith('09') and len(phone_number) == 11:
            return True
            
        return False
    
    def _normalize_phone_number(self, phone_number):
        """Normalize phone number to international format"""
        if not phone_number:
            return None
            
        phone_number = phone_number.strip()
        
        if phone_number.startswith('+'):
            return phone_number
            
        if phone_number.startswith('09') and len(phone_number) == 11:
            return f"+98{phone_number[1:]}"
            
        if phone_number.startswith('9') and len(phone_number) == 10:
            return f"+98{phone_number}"
            
        return phone_number
    
    def send_sms(self, recipients, message, send_time=None, sending_type="webservice"):
        """Send SMS to multiple recipients"""
        
        if not recipients or not isinstance(recipients, list):
            return {'status': False, 'error': 'Recipients must be a non-empty list'}
            
        if not message or not message.strip():
            return {'status': False, 'error': 'Message cannot be empty'}
            
        valid_recipients = []
        for recipient in recipients:
            if self._validate_phone_number(recipient):
                valid_recipients.append(recipient)
            else:
                logger.warning(f"Invalid phone number format: {recipient}")
                
        if not valid_recipients:
            return {'status': False, 'error': 'No valid phone numbers provided'}
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        payload = {
            "sending_type": sending_type,
            "from_number": self.from_number,
            "message": message.strip(),
            "params": {"recipients": valid_recipients}
        }
        
        if send_time:
            try:
                datetime.strptime(send_time, '%Y-%m-%d %H:%M:%S')
                payload["send_time"] = send_time
            except ValueError:
                logger.warning(f"Invalid datetime format: {send_time}. Sending immediately.")
        
        logger.info(f"Sending SMS to {len(valid_recipients)} recipients")
        logger.info(f"api token is {self.api_key} recipients")
        
        result = self._make_request('POST', '/api/send', headers, payload)
        
        if result['status']:
            logger.info(f"SMS sent successfully to {len(valid_recipients)} recipients")
            return {
                'status': True,
                'message': f'SMS sent successfully to {len(valid_recipients)} recipients',
                'data': result['data']
            }
        else:
            logger.error(f"SMS sending failed: {result.get('error', 'Unknown error')}")
            return result
    
    def send_otp_sms(self, phone_number, otp_code):
        """Send OTP verification code via SMS"""
        if not otp_code or not otp_code.strip():
            return {'status': False, 'error': 'OTP code cannot be empty'}
            
        message = f"کد تایید شما: {otp_code}"
        
        normalized_number = self._normalize_phone_number(phone_number)
        if not normalized_number:
            return {'status': False, 'error': 'Invalid phone number format'}
            
        return self.send_sms([normalized_number], message)
    
    def send_welcome_sms(self, phone_number, user_name=None):
        """Send welcome message after successful registration"""
        if user_name and user_name.strip():
            message = f"سلام {user_name} عزیز! به آنشو خوش آمدید. ثبت نام شما با موفقیت انجام شد."
        else:
            message = "سلام! به آنشو خوش آمدید. ثبت نام شما با موفقیت انجام شد."
            
        normalized_number = self._normalize_phone_number(phone_number)
        if not normalized_number:
            return {'status': False, 'error': 'Invalid phone number format'}
            
        return self.send_sms([normalized_number], message)

def test_sms_service():
    """Test the SMS service functionality"""
    
    print("🧪 Testing SMS Service...")
    print("=" * 50)
    
    # Initialize SMS service
    sms_service = SMSService()
    
    # Test 1: Phone number validation
    print("\n1️⃣ Testing phone number validation...")
    test_numbers = [
        "+989120000000",  # Valid international
        "09120000000",    # Valid Iranian
        "9120000000",     # Valid Iranian without leading 0
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