#!/usr/bin/env python
"""
Simple Standards Seed Data Script
This script reads the استاندارد ها.xlsx file and creates Standards records.
Run with: python3 seed_standards_simple.py
"""

import os
import sys
import django
import pandas as pd
from datetime import datetime
from django.utils import timezone
from django.utils.text import slugify

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mahoverse.settings')
django.setup()

from course.models import Standards

def clean_value(value):
    """Clean and convert values"""
    if pd.isna(value) or value == '-' or value == '':
        return None
    if isinstance(value, (int, float)):
        if pd.isna(value):
            return None
        return value
    return str(value).strip()

def parse_date(date_value):
    """Parse date values safely"""
    if pd.isna(date_value) or date_value == '-' or date_value == '':
        return None
    
    try:
        # Handle different date formats
        if isinstance(date_value, str):
            # Try parsing Persian date format (1401/03/10)
            if '/' in date_value and len(date_value.split('/')) == 3:
                parts = date_value.split('/')
                if len(parts[0]) == 4:  # Persian year format
                    # Convert Persian year to Gregorian (approximate)
                    persian_year = int(parts[0])
                    gregorian_year = persian_year + 621
                    month = int(parts[1])
                    day = int(parts[2])
                    return datetime(gregorian_year, month, day).date()
        
        # Try pandas date parsing
        if hasattr(date_value, 'date'):
            return date_value.date()
        
        # Try string parsing
        return pd.to_datetime(date_value).date()
    except:
        return None

def create_standards_from_excel():
    """Create standards from Excel file"""
    try:
        # Read the Excel file
        excel_file = 'استاندارد ها.xlsx'
        if not os.path.exists(excel_file):
            print(f"❌ Excel file '{excel_file}' not found!")
            return
        
        print("📖 Reading Excel file...")
        
        # Read with header in row 1 (index 1)
        df = pd.read_excel(excel_file, header=1)
        print(f"✅ Successfully read Excel file with {len(df)} rows")
        
        # Remove rows where all values are NaN
        df = df.dropna(how='all')
        print(f"After removing empty rows: {len(df)} rows")
        
        # Clear existing standards
        print("🗑️ Clearing existing standards...")
        Standards.objects.all().delete()
        
        created_count = 0
        error_count = 0
        
        print("📝 Creating standards...")
        
        for index, row in df.iterrows():
            try:
                # Extract data from row
                standard_data = {
                    'number': clean_value(row.iloc[0]) if len(row) > 0 else None,
                    'cluster': clean_value(row.iloc[1]) if len(row) > 1 else None,
                    'group_name': clean_value(row.iloc[2]) if len(row) > 2 else None,
                    'standard_name': clean_value(row.iloc[3]) if len(row) > 3 else None,
                    'old_standard_code': clean_value(row.iloc[4]) if len(row) > 4 else None,
                    'version': clean_value(row.iloc[5]) if len(row) > 5 else None,
                    'competency_code': clean_value(row.iloc[6]) if len(row) > 6 else None,
                    'isco_job_code': clean_value(row.iloc[7]) if len(row) > 7 else None,
                    'isco_group_code': clean_value(row.iloc[8]) if len(row) > 8 else None,
                    'entry_education_level': clean_value(row.iloc[9]) if len(row) > 9 else None,
                    'theoretical_hours': clean_value(row.iloc[10]) if len(row) > 10 else None,
                    'practical_hours': clean_value(row.iloc[11]) if len(row) > 11 else None,
                    'internship_hours': clean_value(row.iloc[12]) if len(row) > 12 else None,
                    'project_hours': clean_value(row.iloc[13]) if len(row) > 13 else None,
                    'total_hours': clean_value(row.iloc[14]) if len(row) > 14 else None,
                    'work_and_knowledge': clean_value(row.iloc[15]) if len(row) > 15 else None,
                    'type': clean_value(row.iloc[16]) if len(row) > 16 else None,
                    'standard_name_latin': clean_value(row.iloc[17]) if len(row) > 17 else None,
                    'compilation_date': parse_date(row.iloc[18]) if len(row) > 18 else None,
                }
                
                # Skip if no essential data
                if not standard_data['standard_name'] and not standard_data['number']:
                    continue
                
                # Create the standard
                standard = Standards.objects.create(**standard_data)
                created_count += 1
                
                if created_count % 100 == 0:
                    print(f"✅ Created {created_count} standards...")
                    
            except Exception as e:
                error_count += 1
                if error_count <= 10:  # Only show first 10 errors
                    print(f"❌ Error processing row {index}: {str(e)}")
                continue
        
        print(f"\n🎉 Standards creation completed!")
        print(f"- Created: {created_count} standards")
        print(f"- Errors: {error_count} rows")
        print(f"- Total standards in database: {Standards.objects.count()}")
        
    except Exception as e:
        print(f"❌ Error creating standards seed data: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    """Main function"""
    print("🚀 Starting Standards Seed Data Creation...")
    create_standards_from_excel()
    print("✅ Seed data creation completed!")

if __name__ == "__main__":
    main()
