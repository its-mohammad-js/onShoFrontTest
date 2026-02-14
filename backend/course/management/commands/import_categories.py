import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
import os

from course.models import Category


class Command(BaseCommand):
    help = "Import hierarchical categories from Excel file. E=parent, D=child of E, C/B/A=children of D. Deletes all existing categories first."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="categories.xlsx",
            help="Path to Excel file (default: categories.xlsx)"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        # Get file path
        path = options["file"]
        
        # If relative path, check in current directory
        if not os.path.isabs(path):
            if not os.path.exists(path):
                self.stdout.write(self.style.ERROR(f"❌ File not found: {path}"))
                return
        
        # Step 1: Delete all existing categories
        self.stdout.write("🧹 Deleting all existing categories...")
        deleted_count = Category.objects.all().count()
        Category.objects.all().delete()
        self.stdout.write(self.style.WARNING(f"   Deleted {deleted_count} existing categories"))

        # Step 2: Read Excel file
        try:
            df = pd.read_excel(path, header=None)
            self.stdout.write(f"📘 Loaded {len(df)} rows from {path}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error reading Excel file: {e}"))
            return

        # Define columns (0-based index: A=0, B=1, C=2, D=3, E=4)
        COL_A, COL_B, COL_C, COL_D, COL_E = 0, 1, 2, 3, 4

        # Step 3: Cache to prevent duplicates
        # cache_e: stores E column values (top-level parents) - key: title, value: Category object
        # cache_d: stores D column values per E parent - key: (e_id, d_title), value: Category object
        cache_e = {}
        cache_d = {}

        def clean_title(title):
            """Clean and validate title"""
            if pd.isna(title) or not str(title).strip():
                return None
            return str(title).strip()

        def get_or_create_parent_e(title):
            """Get or create top-level parent from column E (no duplicates)"""
            title = clean_title(title)
            if not title:
                return None
            
            if title in cache_e:
                return cache_e[title]
            
            obj, created = Category.objects.get_or_create(
                title=title,
                parent=None,
                defaults={'parent': None}
            )
            cache_e[title] = obj
            if created:
                self.stdout.write(f"   ✓ Created parent: {title}")
            return obj

        def get_or_create_child_d(d_title, parent_e):
            """Get or create child from column D under parent E (no duplicates per E)"""
            d_title = clean_title(d_title)
            if not d_title or not parent_e:
                return None
            
            # Don't import if D value is same as E value (repeated column)
            if d_title == parent_e.title:
                return None
            
            cache_key = (parent_e.id, d_title)
            if cache_key in cache_d:
                return cache_d[cache_key]
            
            obj, created = Category.objects.get_or_create(
                title=d_title,
                parent=parent_e,
                defaults={'parent': parent_e}
            )
            cache_d[cache_key] = obj
            if created:
                self.stdout.write(f"   ✓ Created child D: {d_title} (under {parent_e.title})")
            return obj

        def create_children_abc(a_title, b_title, c_title, parent_d):
            """Create children from columns A, B, C under parent D"""
            if not parent_d:
                return
            
            created_count = 0
            for title in [a_title, b_title, c_title]:
                title = clean_title(title)
                if not title:
                    continue
                
                obj, created = Category.objects.get_or_create(
                    title=title,
                    parent=parent_d,
                    defaults={'parent': parent_d}
                )
                if created:
                    created_count += 1
                    self.stdout.write(f"   ✓ Created child A/B/C: {title} (under {parent_d.title})")
            
            return created_count

        # Step 4: Process each row and create hierarchy
        total_created = 0
        for idx, row in df.iterrows():
            e_title = row[COL_E]
            d_title = row[COL_D]
            a_title = row[COL_A]
            b_title = row[COL_B]
            c_title = row[COL_C]

            # Skip rows where E is empty
            if pd.isna(e_title) or not str(e_title).strip():
                continue

            # Create hierarchy: E -> D -> A/B/C
            parent_e = get_or_create_parent_e(e_title)
            if parent_e:
                child_d = get_or_create_child_d(d_title, parent_e)
                if child_d:
                    created = create_children_abc(a_title, b_title, c_title, child_d)
                    total_created += (created or 0)

        # Summary
        total_categories = Category.objects.count()
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"✅ Import completed successfully!"))
        self.stdout.write(f"   Total categories in database: {total_categories}")
        self.stdout.write(f"   Top-level parents (E): {len(cache_e)}")
        self.stdout.write(f"   Second-level children (D): {len(cache_d)}")
