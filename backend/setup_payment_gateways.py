#!/usr/bin/env python3
"""
Setup Payment Gateways for Mahoverse
This script creates default payment gateway configurations
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mahoverse.settings')
django.setup()

from payment.models import PaymentGateway, Status, Situation

def setup_payment_gateways():
    print("🔧 Setting up payment gateways...")
    
    # Create Zarinpal gateway
    zarinpal, created = PaymentGateway.objects.get_or_create(
        name='zarinpal',
        defaults={
            'display_name': 'زرین‌پال',
            'is_active': True,
            'is_sandbox': True,
            'config': {
                'merchant_id': '',
                'sandbox': True,
                'description': 'پرداخت امن با زرین‌پال'
            }
        }
    )
    
    if created:
        print("✅ Zarinpal gateway created")
    else:
        print("ℹ️  Zarinpal gateway already exists")
    
    # Create IDPay gateway
    idpay, created = PaymentGateway.objects.get_or_create(
        name='idpay',
        defaults={
            'display_name': 'آیدی‌پی',
            'is_active': True,
            'is_sandbox': True,
            'config': {
                'api_key': '',
                'sandbox': True,
                'description': 'پرداخت امن با آیدی‌پی'
            }
        }
    )
    
    if created:
        print("✅ IDPay gateway created")
    else:
        print("ℹ️  IDPay gateway already exists")
    
    print("🎉 Payment gateways setup completed!")

def setup_payment_statuses():
    print("🔧 Setting up payment statuses...")
    
    # Create payment statuses
    statuses = [
        ('در-حال-پرداخت', 'در حال پرداخت'),
        ('پرداخت-شده', 'پرداخت شده'),
        ('لغو-شده', 'لغو شده'),
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    for slug, title in statuses:
        status, created = Status.objects.get_or_create(
            slug=slug,
            defaults={'title': title}
        )
        if created:
            print(f"✅ Status created: {title}")
        else:
            print(f"ℹ️  Status already exists: {title}")
    
    print("🎉 Payment statuses setup completed!")

def setup_transaction_situations():
    print("🔧 Setting up transaction situations...")
    
    # Create transaction situations
    situations = [
        ('pending', 'در انتظار پرداخت'),
        ('success', 'پرداخت موفق'),
        ('failed', 'پرداخت ناموفق'),
        ('cancelled', 'لغو شده توسط کاربر'),
        ('refunded', 'برگشت شده'),
    ]
    
    for slug, title in situations:
        situation, created = Situation.objects.get_or_create(
            slug=slug,
            defaults={'title': title}
        )
        if created:
            print(f"✅ Situation created: {title}")
        else:
            print(f"ℹ️  Situation already exists: {title}")
    
    print("🎉 Transaction situations setup completed!")

def main():
    print("🚀 Starting payment system setup...")
    print("=" * 50)
    
    try:
        setup_payment_gateways()
        print()
        setup_payment_statuses()
        print()
        setup_transaction_situations()
        print()
        
        print("=" * 50)
        print("✅ Payment system setup completed successfully!")
        print()
        print("📋 Next steps:")
        print("1. Set your payment gateway credentials in environment variables:")
        print("   - ZARINPAL_MERCHANT_ID=your_merchant_id")
        print("   - IDPAY_API_KEY=your_api_key")
        print("2. Configure PAYMENT_GATEWAY=zarinpal or PAYMENT_GATEWAY=idpay")
        print("3. Set SANDBOX=False for production")
        print()
        print("🔗 Payment Gateway URLs:")
        print("- Zarinpal: https://zarinpal.com")
        print("- IDPay: https://idpay.ir")
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
