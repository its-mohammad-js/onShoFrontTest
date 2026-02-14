import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
import os
from datetime import datetime
from course.models import Standards, Category


def parse_persian_date(date_str):
    """Parse Persian date string like '1393/06/01' to Python date"""
    if pd.isna(date_str) or not date_str or str(date_str).strip() == '':
        return None
    
    try:
        date_str = str(date_str).strip()
        parts = date_str.split('/')
        if len(parts) == 3:
            year = int(parts[0])
            month = int(parts[1])
            day = int(parts[2])
            
            # Convert Persian year to Gregorian (approximate)
            gregorian_year = year + 621
            
            # Try to create date
            try:
                return datetime(gregorian_year, month, day).date()
            except ValueError:
                # If day is invalid, use first day of month
                return datetime(gregorian_year, month, 1).date()
    except:
        pass
    return None


def clean_value(value):
    """Clean and convert value"""
    if pd.isna(value):
        return None
    value = str(value).strip()
    if value == '' or value.lower() == 'nan':
        return None
    return value


def safe_int(value):
    """Safely convert to int"""
    try:
        if pd.isna(value):
            return None
        return int(float(value))
    except:
        return None


class Command(BaseCommand):
    help = "Import standards data from Excel file (codes.xlsx)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="codes.xlsx",
            help="Path to Excel file (default: codes.xlsx)"
        )
        parser.add_argument(
            "--update",
            action="store_true",
            help="Update existing standards if old_standard_code matches"
        )

    def handle(self, *args, **options):
        path = options["file"]
        update_existing = options.get("update", False)
        
        if not os.path.isabs(path):
            if not os.path.exists(path):
                self.stdout.write(self.style.ERROR(f"File not found: {path}"))
                return
        
        try:
            # Read Excel file, skip first 2 rows (headers)
            df = pd.read_excel(path, header=None, skiprows=2)
            self.stdout.write(f"Loaded {len(df)} rows from {path}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading Excel file: {e}"))
            return
        
        imported_count = 0
        updated_count = 0
        skipped_count = 0
        
        # Column indices (0-based)
        COL_NUMBER = 0          # شماره
        COL_CLUSTER = 1         # خوشه
        COL_GROUP_NAME = 2      # نام گروه
        COL_STANDARD_NAME = 3   # نام استاندارد
        COL_OLD_CODE = 4        # کد استاندارد قدیم
        COL_VERSION = 5         # نسخه
        COL_COMPETENCY = 6      # کد شایستگی
        COL_ISCO_JOB = 9        # کد شغل
        COL_ISCO_GROUP = 12     # کد گروه
        COL_SKILL_LEVEL = 15    # سطح مهارت
        COL_ISCO_CODE = 16      # کد ISCO
        COL_ENTRY_EDU = 21      # سطح تحصیلات ورودی
        COL_THEORETICAL = 22    # ساعت نظری
        COL_PRACTICAL = 23      # ساعت عملی
        COL_INTERNSHIP = 24     # ساعت کارورزی
        COL_PROJECT = 25        # ساعت پروژه
        COL_TOTAL = 26          # ساعت کل
        COL_WORK_KNOWLEDGE = 27 # کارو دانش
        COL_TYPE = 28           # نوع
        COL_STANDARD_LATIN = 29 # نام استاندارد به لاتین
        COL_COMPILATION_DATE = 30  # تاریخ تدوین
        
        # Process each row individually to avoid transaction issues
        total_rows = len(df)
        
        for idx, row in df.iterrows():
            try:
                # Each row in its own transaction
                with transaction.atomic():
                            old_code = clean_value(row[COL_OLD_CODE])
                            standard_name = clean_value(row[COL_STANDARD_NAME])
                            number = safe_int(row[COL_NUMBER])
                            
                            # Skip if no standard_name and no number
                            if not standard_name and not number:
                                skipped_count += 1
                                continue
                            
                            # If no old_code, create a unique identifier from number and standard_name
                            original_old_code = old_code
                            if not old_code:
                                if number and standard_name:
                                    old_code = f"AUTO-{number}-{hash(standard_name) % 10000}"
                                elif number:
                                    old_code = f"AUTO-{number}"
                                elif standard_name:
                                    old_code = f"AUTO-{hash(standard_name) % 100000}"
                                else:
                                    skipped_count += 1
                                    continue
                            
                            # Check if standard with this old_code already exists
                            existing = None
                            if original_old_code:
                                # If has original old_code, check by it
                                existing = Standards.objects.filter(old_standard_code=original_old_code).first()
                            
                            # Also check by number and standard_name
                            if not existing and number and standard_name:
                                existing = Standards.objects.filter(
                                    number=number,
                                    standard_name=standard_name
                                ).first()
                            
                            # If still not found, check by old_code (auto-generated)
                            if not existing:
                                existing = Standards.objects.filter(old_standard_code=old_code).first()
                            
                            # Always update if exists, or create if not
                            standard_data = {
                                'number': safe_int(row[COL_NUMBER]),
                                'cluster': clean_value(row[COL_CLUSTER]),
                                'group_name': clean_value(row[COL_GROUP_NAME]),
                                'standard_name': clean_value(row[COL_STANDARD_NAME]),
                                'old_standard_code': old_code,
                                'version': safe_int(row[COL_VERSION]),
                                'competency_code': safe_int(row[COL_COMPETENCY]),
                                'isco_job_code': safe_int(row[COL_ISCO_JOB]),
                                'isco_group_code': safe_int(row[COL_ISCO_GROUP]),
                                'entry_education_level': clean_value(row[COL_ENTRY_EDU]),
                                'theoretical_hours': safe_int(row[COL_THEORETICAL]),
                                'practical_hours': safe_int(row[COL_PRACTICAL]),
                                'internship_hours': safe_int(row[COL_INTERNSHIP]),
                                'project_hours': safe_int(row[COL_PROJECT]),
                                'total_hours': safe_int(row[COL_TOTAL]),
                                'work_and_knowledge': clean_value(row[COL_WORK_KNOWLEDGE]) or 'هیچ کدام',
                                'type': clean_value(row[COL_TYPE]) or 'شغل',
                                'standard_name_latin': clean_value(row[COL_STANDARD_LATIN]),
                                'compilation_date': parse_persian_date(row[COL_COMPILATION_DATE]),
                            }
                            
                            if existing:
                                # Update existing - always update to get latest data
                                for key, value in standard_data.items():
                                    setattr(existing, key, value)
                                existing.save()
                                updated_count += 1
                            else:
                                # Create new
                                Standards.objects.create(**standard_data)
                                imported_count += 1
                                
            except Exception as e:
                error_msg = str(e)
                # Only show detailed error for first few errors to avoid spam
                if skipped_count < 10:
                    self.stdout.write(self.style.WARNING(f"Error processing row {idx + 3}: {error_msg[:150]}"))
                skipped_count += 1
                continue
            
            # Progress message every 500 rows
            if (idx + 1) % 500 == 0 or (idx + 1) == total_rows:
                self.stdout.write(f"Processed {idx + 1}/{total_rows} rows... (Imported: {imported_count}, Updated: {updated_count}, Skipped: {skipped_count})")
        
        self.stdout.write(self.style.SUCCESS(f"\nImport completed!"))
        self.stdout.write(f"   Imported: {imported_count}")
        self.stdout.write(f"   Updated: {updated_count}")
        self.stdout.write(f"   Skipped: {skipped_count}")
        self.stdout.write(f"   Total processed: {imported_count + updated_count + skipped_count}")

