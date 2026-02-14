import requests
import json
from django.conf import settings
from django.urls import reverse


class ZarinpalGateway:
    """
    Zarinpal Payment Gateway Integration
    """
    
    # Zarinpal API URLs
    SANDBOX_URL = "https://sandbox.zarinpal.com/pg/rest/WebGate/"
    PRODUCTION_URL = "https://api.zarinpal.com/pg/rest/WebGate/"
    
    def __init__(self, merchant_id=None, sandbox=True):
        self.merchant_id = merchant_id or getattr(settings, 'ZARINPAL_MERCHANT_ID', '')
        self.sandbox = sandbox
        self.base_url = self.SANDBOX_URL if sandbox else self.PRODUCTION_URL
    
    def create_payment_request(self, amount, description, callback_url, mobile=None, email=None):
        """
        Create a payment request with Zarinpal
        """
        data = {
            "merchant_id": self.merchant_id,
            "amount": amount,  # Amount in Toman
            "description": description,
            "callback_url": callback_url,
        }
        
        if mobile:
            data["mobile"] = mobile
        if email:
            data["email"] = email
            
        try:
            response = requests.post(
                f"{self.base_url}PaymentRequest.json",
                data=json.dumps(data),
                headers={'Content-Type': 'application/json'}
            )
            
            result = response.json()
            
            if result.get('data', {}).get('code') == 100:
                return {
                    'success': True,
                    'authority': result['data']['authority'],
                    'payment_url': f"https://{'sandbox.' if self.sandbox else ''}zarinpal.com/pg/StartPay/{result['data']['authority']}"
                }
            else:
                return {
                    'success': False,
                    'error': result.get('errors', {}).get('message', 'خطا در ایجاد درخواست پرداخت')
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'خطا در ارتباط با درگاه پرداخت: {str(e)}'
            }
    
    def verify_payment(self, authority, amount):
        """
        Verify payment with Zarinpal
        """
        data = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "authority": authority
        }
        
        try:
            response = requests.post(
                f"{self.base_url}PaymentVerification.json",
                data=json.dumps(data),
                headers={'Content-Type': 'application/json'}
            )
            
            result = response.json()
            
            if result.get('data', {}).get('code') == 100:
                return {
                    'success': True,
                    'ref_id': result['data']['ref_id'],
                    'card_pan': result['data'].get('card_pan', ''),
                    'card_hash': result['data'].get('card_hash', ''),
                    'fee_type': result['data'].get('fee_type', ''),
                    'fee': result['data'].get('fee', 0)
                }
            else:
                return {
                    'success': False,
                    'error': result.get('errors', {}).get('message', 'خطا در تایید پرداخت')
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'خطا در تایید پرداخت: {str(e)}'
            }


class IDPayGateway:
    """
    IDPay Payment Gateway Integration
    """
    
    SANDBOX_URL = "https://api.idpay.ir/v1.1/"
    PRODUCTION_URL = "https://api.idpay.ir/v1.1/"
    
    def __init__(self, api_key=None, sandbox=True):
        self.api_key = api_key or getattr(settings, 'IDPAY_API_KEY', '')
        self.sandbox = sandbox
        self.base_url = self.SANDBOX_URL if sandbox else self.PRODUCTION_URL
    
    def create_payment_request(self, amount, order_id, description, callback_url, name=None, phone=None, mail=None):
        """
        Create a payment request with IDPay
        """
        data = {
            "order_id": str(order_id),
            "amount": amount,  # Amount in Rial
            "name": name or "",
            "phone": phone or "",
            "mail": mail or "",
            "desc": description,
            "callback": callback_url
        }
        
        try:
            response = requests.post(
                f"{self.base_url}payment",
                data=json.dumps(data),
                headers={
                    'Content-Type': 'application/json',
                    'X-API-KEY': self.api_key,
                    'X-SANDBOX': '1' if self.sandbox else '0'
                }
            )
            
            result = response.json()
            
            if result.get('id'):
                return {
                    'success': True,
                    'payment_id': result['id'],
                    'payment_url': result['link']
                }
            else:
                return {
                    'success': False,
                    'error': result.get('error_message', 'خطا در ایجاد درخواست پرداخت')
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'خطا در ارتباط با درگاه پرداخت: {str(e)}'
            }
    
    def verify_payment(self, payment_id, order_id):
        """
        Verify payment with IDPay
        """
        data = {
            "id": payment_id,
            "order_id": str(order_id)
        }
        
        try:
            response = requests.post(
                f"{self.base_url}payment/verify",
                data=json.dumps(data),
                headers={
                    'Content-Type': 'application/json',
                    'X-API-KEY': self.api_key,
                    'X-SANDBOX': '1' if self.sandbox else '0'
                }
            )
            
            result = response.json()
            
            if result.get('status') == 100:
                return {
                    'success': True,
                    'track_id': result.get('track_id'),
                    'payment_id': result.get('id'),
                    'order_id': result.get('order_id'),
                    'amount': result.get('amount'),
                    'date': result.get('date')
                }
            else:
                return {
                    'success': False,
                    'error': result.get('error_message', 'خطا در تایید پرداخت')
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'خطا در تایید پرداخت: {str(e)}'
            }
