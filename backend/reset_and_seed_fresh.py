#!/usr/bin/env python
"""
Script to reset database and run fresh seed data
This will clear existing data and create new comprehensive seed data
Works with both SQLite and PostgreSQL
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mahoverse.settings')
django.setup()

from clear_all_data import clear_all_data
from seed_data import main


if __name__ == '__main__':
    print("🚀 Starting fresh database setup...")
    print("=" * 60)
    print()
    
    try:
        # Clear all existing data
        clear_all_data()
        print()
        
        # Create fresh seed data
        print("🌱 Creating fresh seed data...")
        print("=" * 60)
        main()
        
        print()
        print("=" * 60)
        print("🎉 Fresh database setup completed successfully!")
        print("✨ Your database now has fresh seed data!")
        print("🔗 You can now run your Django server and see the results!")
        
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ Error during setup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

