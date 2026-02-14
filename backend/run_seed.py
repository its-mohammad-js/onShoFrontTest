#!/usr/bin/env python
"""
Script to run the updated seed data
This will create comprehensive seed data with proper attributes
"""

import os
import sys
import django
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mahoverse.settings')
django.setup()

# Import the seed data functions
from seed_data import main

if __name__ == '__main__':
    print("🌱 Starting comprehensive seed data creation...")
    print("=" * 50)
    
    try:
        main()
        print("=" * 50)
        print("✅ Seed data creation completed successfully!")
        print("🎉 Your courses now have proper attributes and won't show 'نامشخص' anymore!")
        
    except Exception as e:
        print("=" * 50)
        print(f"❌ Error creating seed data: {e}")
        sys.exit(1)
