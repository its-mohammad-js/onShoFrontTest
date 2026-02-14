import os
import requests
import logging
import xml.etree.ElementTree as ET
from datetime import datetime
from django.conf import settings

logger = logging.getLogger(__name__)

class SMSService:
    """
    SMS Service for sending SMS messages using the provided API
    """
    
    def __init__(self):
        self.username = (
            getattr(settings, "MELIPAYAMAK_USERNAME", None)
            or os.getenv("MELIPAYAMAK_USERNAME")
        )
        self.password = (
            getattr(settings, "MELIPAYAMAK_PASSWORD", None)
            or os.getenv("MELIPAYAMAK_PASSWORD")
        )
        self.base_url = "https://api.payamak-panel.com"
        self.from_number = (
            getattr(settings, "MELIPAYAMAK_FROM", None)
            or os.getenv("MELIPAYAMAK_FROM")
        )
        
        self.timeout = 30  # Request timeout in seconds
        self.max_retries = 3  # Maximum number of retries for failed requests
        
    def _make_request(self, method, endpoint, headers=None, json_data=None, params=None, data=None, retries=0):
        """
        Make HTTP request with retry logic and proper error handling
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint
            headers (dict): Request headers
            json_data (dict): JSON data for POST requests
            retries (int): Current retry attempt
            
        Returns:
            dict: Response data or error information
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            logger.info(f"Making {method} request to {url}")
            
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=json_data,
                params=params,
                data=data,
                timeout=self.timeout,
            )
            
            logger.info(f"Response status: {response.status_code}")
            
            # Try to parse JSON response, fallback to text
            try:
                response_data = response.json()
            except ValueError:
                response_data = response.text
            
            if response.status_code == 200:
                logger.info(f"Request successful: {response_data}")
                return {
                    'status': True,
                    'data': response_data
                }
            else:
                logger.error(f"Request failed with status {response.status_code}: {response_data}")
                return {
                    'status': False,
                    'error': f"HTTP {response.status_code}: {response_data}",
                    'data': response_data
                }
                
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout for {url}")
            if retries < self.max_retries:
                logger.info(f"Retrying request (attempt {retries + 1}/{self.max_retries})")
                return self._make_request(method, endpoint, headers, json_data, params, data, retries + 1)
            return {
                'status': False,
                'error': 'Request timeout - please try again later'
            }
            
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error for {url}: {str(e)}")
            if retries < self.max_retries:
                logger.info(f"Retrying request (attempt {retries + 1}/{self.max_retries})")
                return self._make_request(method, endpoint, headers, json_data, params, data, retries + 1)
            return {
                'status': False,
                'error': 'Connection error - please check your internet connection'
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for {url}: {str(e)}")
            return {
                'status': False,
                'error': f'Request failed: {str(e)}'
            }
            
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {str(e)}")
            return {
                'status': False,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def _validate_phone_number(self, phone_number):
        """
        Validate phone number format
        
        Args:
            phone_number (str): Phone number to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not phone_number or not isinstance(phone_number, str):
            return False
            
        # Remove spaces and validate format
        phone_number = phone_number.strip()
        
        # Check if it starts with + and has correct length
        if phone_number.startswith('+'):
            return len(phone_number) >= 11 and len(phone_number) <= 15
        
        # Check if it's a valid Iranian mobile number (starting with 09)
        if phone_number.startswith('09') and len(phone_number) == 11:
            return True
            
        return False

    def _normalize_to_iranian_mobile(self, phone_number):
        """
        Normalize phone number to Iranian mobile format (09xxxxxxxxx)
        """
        if not phone_number:
            return None

        number = phone_number.strip().replace(" ", "")

        if number.startswith("+98"):
            number = "0" + number[3:]
        elif number.startswith("0098"):
            number = "0" + number[4:]
        elif number.startswith("98") and len(number) == 12:
            number = "0" + number[2:]
        elif number.startswith("9") and len(number) == 10:
            number = "0" + number

        if number.startswith("09") and len(number) == 11:
            return number

        return None
    
    def _validate_datetime_format(self, datetime_str):
        """
        Validate datetime string format
        
        Args:
            datetime_str (str): Datetime string to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
            return True
        except ValueError:
            return False
    
    def _normalize_phone_number(self, phone_number):
        """
        Normalize phone number to international format
        
        Args:
            phone_number (str): Phone number to normalize
            
        Returns:
            str: Normalized phone number
        """
        if not phone_number:
            return None
            
        phone_number = phone_number.strip()
        
        # If already in international format
        if phone_number.startswith('+'):
            return phone_number
            
        # Convert Iranian mobile number to international format
        if phone_number.startswith('09') and len(phone_number) == 11:
            return f"+98{phone_number[1:]}"
            
        # If it starts with 9 and has 10 digits, assume it's Iranian
        if phone_number.startswith('9') and len(phone_number) == 10:
            return f"+98{phone_number}"
            
        return phone_number
    
    def send_sms(self, recipients, message, send_time=None, sending_type="webservice"):
        """
        Send SMS to multiple recipients
        
        Args:
            recipients (list): List of phone numbers (e.g., ["+989120000000", "+989350000000"])
            message (str): The message text to send
            send_time (str, optional): Scheduled send time in format "YYYY-MM-DD HH:MM:SS"
            sending_type (str): Type of sending (default: "webservice")
            
        Returns:
            dict: Response from the API
        """
        
        # Validate inputs
        if not recipients or not isinstance(recipients, list):
            return {
                'status': False,
                'error': 'Recipients must be a non-empty list'
            }
            
        if not message or not message.strip():
            return {
                'status': False,
                'error': 'Message cannot be empty'
            }
            
        # Validate phone numbers
        valid_recipients = []
        for recipient in recipients:
            if self._validate_phone_number(recipient):
                valid_recipients.append(recipient)
            else:
                logger.warning(f"Invalid phone number format: {recipient}")
                
        if not valid_recipients:
            return {
                'status': False,
                'error': 'No valid phone numbers provided'
            }
        
        if not self.username or not self.password:
            return {
                'status': False,
                'error': 'SMS credentials are not configured (MELIPAYAMAK_USERNAME/PASSWORD)'
            }

        if not self.from_number or not str(self.from_number).strip():
            return {
                'status': False,
                'error': 'SMS sender number is not configured (MELIPAYAMAK_FROM)'
            }

        normalized_recipients = []
        for recipient in valid_recipients:
            normalized = self._normalize_to_iranian_mobile(recipient)
            if normalized:
                normalized_recipients.append(normalized)
            else:
                logger.warning(f"Invalid Iranian mobile number format: {recipient}")

        if not normalized_recipients:
            return {
                'status': False,
                'error': 'No valid Iranian mobile numbers provided'
            }

        if send_time and not self._validate_datetime_format(send_time):
            logger.warning(f"Invalid datetime format: {send_time}. Sending immediately.")

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        error_messages = {
            -110: 'API key required instead of password',
            -109: 'Allowed IP not configured for API access',
            -108: 'IP blocked due to failed attempts',
            0: 'Invalid username or password',
            2: 'Insufficient credit',
            3: 'Daily sending limit',
            4: 'Sending volume limit',
            5: 'Invalid sender number',
            6: 'Service is updating',
            7: 'Message contains filtered words',
            9: 'Public lines not allowed via web service',
            10: 'User is not active',
            11: 'Not sent',
            12: 'User documents are incomplete',
            14: 'Message contains a link',
            15: 'Multiple recipients require "لغو11" in message',
            16: 'Recipient number not found',
            17: 'Message text is empty',
            18: 'Recipient number is invalid',
            35: 'Recipient is in telecom blacklist',
        }

        results = []
        for recipient in normalized_recipients:
            payload = {
                "username": self.username,
                "password": self.password,
                "from": str(self.from_number).strip(),
                "to": recipient,
                "text": message.strip(),
                "isflash": "false",
            }

            logger.info(
                "Sending SMS via Melipayamak (to=%s, from=%s, text=%s, endpoint=%s)",
                recipient,
                payload["from"],
                payload["text"],
                "/post/Send.asmx/SendSimpleSMS2",
            )
            result = self._make_request(
                'POST',
                '/post/Send.asmx/SendSimpleSMS2',
                headers=headers,
                data=payload,
            )

            if not result['status']:
                logger.error(
                    "SMS request failed (to=%s, from=%s, error=%s, data=%s)",
                    recipient,
                    payload["from"],
                    result.get("error"),
                    result.get("data"),
                )
                results.append({
                    'recipient': recipient,
                    'status': False,
                    'error': result.get('error', 'Unknown error'),
                    'data': result.get('data'),
                })
                continue

            response_value = result.get('data')
            if isinstance(response_value, dict):
                response_value = (
                    response_value.get('SendSimpleSMS2Result')
                    or response_value.get('ReturnValue')
                    or response_value.get('message')
                )

            response_text = str(response_value).strip() if response_value is not None else ""
            if response_text.startswith("<"):
                try:
                    root = ET.fromstring(response_text)
                    result_node = root.find(".//{*}SendSimpleSMS2Result")
                    if result_node is not None and result_node.text:
                        response_text = result_node.text.strip()
                    elif root.text:
                        response_text = root.text.strip()
                except ET.ParseError:
                    logger.warning("Unable to parse SOAP response (to=%s)", recipient)

            if response_text.lstrip('-').isdigit():
                code = int(response_text)
                if code > 0:
                    results.append({
                        'recipient': recipient,
                        'status': True,
                        'rec_id': response_text,
                    })
                else:
                    logger.error(
                        "SMS provider returned error code (to=%s, from=%s, code=%s, message=%s)",
                        recipient,
                        payload["from"],
                        code,
                        error_messages.get(code, f'Error code {code}'),
                    )
                    results.append({
                        'recipient': recipient,
                        'status': False,
                        'error': error_messages.get(code, f'Error code {code}'),
                        'code': code,
                    })
            else:
                logger.error(
                    "SMS provider returned unexpected response (to=%s, from=%s, response=%s)",
                    recipient,
                    payload["from"],
                    response_text,
                )
                results.append({
                    'recipient': recipient,
                    'status': False,
                    'error': f'Unexpected response: {response_text}',
                })

        failed = [item for item in results if not item['status']]
        if failed:
            logger.error(f"SMS sending failed for {len(failed)} recipients")
            return {
                'status': False,
                'error': 'Some SMS messages failed to send',
                'data': results,
            }

        logger.info(f"SMS sent successfully to {len(results)} recipients")
        return {
            'status': True,
            'message': f'SMS sent successfully to {len(results)} recipients',
            'data': results,
        }
    
    def send_otp_sms(self, phone_number, otp_code):
        """
        Send OTP verification code via SMS
        
        Args:
            phone_number (str): Recipient phone number
            otp_code (str): The OTP code to send
            
        Returns:
            dict: Response from the API
        """
        if not otp_code or not otp_code.strip():
            return {
                'status': False,
                'error': 'OTP code cannot be empty'
            }
            
        message = f"کد تایید شما: {otp_code}"
        
        # Normalize phone number
        normalized_number = self._normalize_phone_number(phone_number)
        if not normalized_number:
            return {
                'status': False,
                'error': 'Invalid phone number format'
            }
            
        return self.send_sms([normalized_number], message)
    
    def send_welcome_sms(self, phone_number, user_name=None):
        """
        Send welcome message after successful registration
        
        Args:
            phone_number (str): Recipient phone number
            user_name (str, optional): User's name for personalization
            
        Returns:
            dict: Response from the API
        """
        if user_name and user_name.strip():
            message = f"سلام {user_name} عزیز! به آنشو خوش آمدید. ثبت نام شما با موفقیت انجام شد."
        else:
            message = "سلام! به آنشو خوش آمدید. ثبت نام شما با موفقیت انجام شد."
            
        # Normalize phone number
        normalized_number = self._normalize_phone_number(phone_number)
        if not normalized_number:
            return {
                'status': False,
                'error': 'Invalid phone number format'
            }
            
        return self.send_sms([normalized_number], message)