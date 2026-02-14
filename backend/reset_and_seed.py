#!/usr/bin/env python
"""
Script to reset database and run fresh seed data
This will clear existing data and create new comprehensive seed data
"""

import os
import sys
import django
from django.core.management import call_command
from django.db import connection

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mahoverse.settings')
django.setup()

def reset_database():
    """Reset the database by dropping and recreating tables"""
    print("🗑️  Resetting database...")
    
    with connection.cursor() as cursor:
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        # Drop all tables
        for table in tables:
            table_name = table[0]
            if table_name != 'sqlite_sequence':  # Don't drop sqlite_sequence
                cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        
        print("✅ Database reset completed!")

def run_migrations():
    """Run Django migrations"""
    print("🔄 Running migrations...")
    call_command('migrate')
    print("✅ Migrations completed!")

def run_seed_data():
    """Run the seed data creation"""
    print("🌱 Creating seed data...")
    from seed_data import main
    main()
    print("✅ Seed data creation completed!")

if __name__ == '__main__':
    print("🚀 Starting fresh database setup...")
    print("=" * 60)
    
    try:
        # Reset database
        reset_database()
        
        # Run migrations
        run_migrations()
        
        # Create seed data
        run_seed_data()
        
        print("=" * 60)
        print("🎉 Fresh database setup completed successfully!")
        print("✨ Your courses now have proper attributes and realistic data!")
        print("🔗 You can now run your Django server and see the results!")
        
    except Exception as e:
        print("=" * 60)
        print(f"❌ Error during setup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
