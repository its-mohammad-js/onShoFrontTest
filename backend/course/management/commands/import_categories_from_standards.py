import os

import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction

from course.models import Category


class Command(BaseCommand):
    help = (
        "Import categories from 'استاندارد ها.xlsx' with B/C/D hierarchy.\n"
        "B = level 1, C = level 2 (child of B), D = level 3 (child of C).\n"
        "For level-3 categories (column D):\n"
        "  - old_code is taken from column E (if empty, last non-empty E is reused)\n"
        "  - isco_code is concatenation of columns F..T.\n"
        "All existing categories will be deleted before import."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="استاندارد ها.xlsx",
            help="Excel file path (default: 'استاندارد ها.xlsx')",
        )
        parser.add_argument(
            "--start-row",
            type=int,
            default=5,
            help="1-based row index to start reading from (default: 5)",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        path = options["file"]
        start_row = options.get("start_row", 5)

        # Resolve relative path
        if not os.path.isabs(path):
            if not os.path.exists(path):
                self.stdout.write(self.style.ERROR(f"❌ File not found: {path}"))
                return

        # Remove all existing categories
        self.stdout.write("🧹 Deleting all existing categories...")
        existing_count = Category.objects.count()
        Category.objects.all().delete()
        self.stdout.write(self.style.WARNING(f"   Deleted {existing_count} existing categories"))

        # Load Excel
        try:
            # Read without header, we'll use numeric indices
            df = pd.read_excel(path, header=None)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error reading Excel file: {e}"))
            return

        self.stdout.write(f"📘 Loaded {len(df)} rows from {path}")

        # Column indices (0-based): A=0, B=1, C=2, D=3, E=4, F=5, ..., T=19
        COL_B = 1
        COL_C = 2
        COL_D = 3
        COL_E = 4
        COL_F = 5
        COL_T = 19

        # Helpers
        def clean(val):
            if pd.isna(val):
                return None
            s = str(val).strip()
            return s or None

        # Caches to prevent duplicates
        # Level 1 (B): key = title
        level1_cache = {}
        # Level 2 (C): key = (parent_id, title)
        level2_cache = {}

        created_level1 = 0
        created_level2 = 0
        created_level3 = 0

        last_old_code = None  # For re-using previous non-empty E when current E is empty

        # Convert start_row (1-based) to DataFrame index (0-based)
        start_index = max(0, start_row - 1)

        for idx, row in df.iterrows():
            # Skip rows before requested start row
            if idx < start_index:
                continue

            b_title = clean(row[COL_B]) if COL_B in row else None
            c_title = clean(row[COL_C]) if COL_C in row else None
            d_title = clean(row[COL_D]) if COL_D in row else None
            e_code_raw = row[COL_E] if COL_E in row else None

            # If nothing meaningful in B/C/D, skip row
            if not (b_title or c_title or d_title):
                continue

            # --- Level 1: column B ---
            level1_cat = None
            if b_title:
                if b_title in level1_cache:
                    level1_cat = level1_cache[b_title]
                else:
                    level1_cat = Category.objects.create(title=b_title, parent=None)
                    level1_cache[b_title] = level1_cat
                    created_level1 += 1
                    self.stdout.write(f"   ✓ Created level-1 (B): {b_title}")

            # --- Level 2: column C (child of B) ---
            level2_cat = None
            if c_title and level1_cat:
                key = (level1_cat.id, c_title)
                if key in level2_cache:
                    level2_cat = level2_cache[key]
                else:
                    level2_cat = Category.objects.create(title=c_title, parent=level1_cat)
                    level2_cache[key] = level2_cat
                    created_level2 += 1
                    self.stdout.write(f"   ✓ Created level-2 (C): {c_title} (under {level1_cat.title})")

            # --- Prepare old_code for D level from column E ---
            cleaned_e = clean(e_code_raw)
            if cleaned_e:
                last_old_code = cleaned_e

            # --- Level 3: column D (child of C), with old_code & isco_code ---
            if d_title and level2_cat:
                # Build isco_code from columns F..T (right-to-left, concatenated digits)
                isco_parts = []
                for col_idx in range(COL_T, COL_F - 1, -1):
                    if col_idx in row:
                        raw_val = row[col_idx]
                        if pd.isna(raw_val):
                            continue
                        # Try to normalize numeric values like 1.0 -> "1"
                        part = None
                        try:
                            part = str(int(float(raw_val)))
                        except Exception:
                            part = clean(raw_val)
                        if part:
                            isco_parts.append(part)

                # Join without any separator, e.g. 7 1 2 7 ... -> "7127..."
                isco_code_value = "".join(isco_parts) if isco_parts else None
                old_code_value = last_old_code

                cat = Category.objects.create(
                    title=d_title,
                    parent=level2_cat,
                    old_code=old_code_value,
                    isco_code=isco_code_value,
                )
                created_level3 += 1
                self.stdout.write(
                    f"   ✓ Created level-3 (D): {d_title} (under {level2_cat.title}) "
                    f"[old_code={old_code_value}, isco_code={'...' if isco_code_value else 'None'}]"
                )

        total = Category.objects.count()
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("✅ Category import from standards completed successfully"))
        self.stdout.write(f"   Level-1 created (B): {created_level1}")
        self.stdout.write(f"   Level-2 created (C): {created_level2}")
        self.stdout.write(f"   Level-3 created (D): {created_level3}")
        self.stdout.write(f"   Total categories in DB: {total}")

