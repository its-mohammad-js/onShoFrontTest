import os
from pathlib import Path
from difflib import SequenceMatcher

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.text import slugify
from django.core.files import File

from course.models import Category


class Command(BaseCommand):
    help = (
        "Set category logos from files in media/category directory.\n"
        "For each file in media/category, finds categories with matching title or slug,\n"
        "sets the logo to that file and enables home_page display."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--category-dir",
            type=str,
            default=None,
            help="Path to category images directory (default: media/category relative to BASE_DIR)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be done without actually updating categories",
        )
        parser.add_argument(
            "--similarity-threshold",
            type=float,
            default=0.5,
            help="Minimum similarity score (0.0-1.0) to match a category (default: 0.5)",
        )

    def handle(self, *args, **options):
        # Determine category directory path
        if options["category_dir"]:
            category_dir = Path(options["category_dir"])
        else:
            # Default to media/category relative to BASE_DIR
            category_dir = Path(settings.BASE_DIR) / "media" / "category"

        if not category_dir.exists():
            self.stdout.write(
                self.style.ERROR(f"❌ Directory not found: {category_dir}")
            )
            return

        if not category_dir.is_dir():
            self.stdout.write(
                self.style.ERROR(f"❌ Path is not a directory: {category_dir}")
            )
            return

        self.stdout.write(f"📁 Scanning directory: {category_dir}")
        
        dry_run = options["dry_run"]
        if dry_run:
            self.stdout.write(self.style.WARNING("🔍 DRY RUN MODE - No changes will be made"))

        # Get all image files in the directory
        image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
        image_files = [
            f for f in category_dir.iterdir()
            if f.is_file() and f.suffix.lower() in image_extensions
        ]

        if not image_files:
            self.stdout.write(
                self.style.WARNING(f"⚠️  No image files found in {category_dir}")
            )
            return

        self.stdout.write(f"📸 Found {len(image_files)} image file(s)")
        
        similarity_threshold = options.get("similarity_threshold", 0.5)
        self.stdout.write(f"🎯 Similarity threshold: {similarity_threshold}")

        # Load all categories once for better performance
        all_categories = list(Category.objects.all())
        self.stdout.write(f"📋 Loaded {len(all_categories)} categories from database")

        updated_count = 0
        not_found_count = 0

        for image_file in image_files:
            # Get filename without extension
            filename_without_ext = image_file.stem  # e.g., "الکترونیک" from "الکترونیک.png"
            
            self.stdout.write(f"\n🔍 Processing: {image_file.name}")
            self.stdout.write(f"   Filename (without ext): {filename_without_ext}")

            category = None
            match_type = None
            similarity_score = 0.0

            # First, try exact matches (title, slug, case-insensitive)
            exact_category = Category.objects.filter(title=filename_without_ext).first()
            if exact_category:
                category = exact_category
                match_type = "exact title"
                similarity_score = 1.0
            else:
                filename_slug = slugify(filename_without_ext, allow_unicode=True)
                exact_category = Category.objects.filter(slug=filename_slug).first()
                if exact_category:
                    category = exact_category
                    match_type = "exact slug"
                    similarity_score = 1.0
                else:
                    exact_category = Category.objects.filter(title__iexact=filename_without_ext).first()
                    if exact_category:
                        category = exact_category
                        match_type = "case-insensitive title"
                        similarity_score = 1.0

            # If no exact match, find the most similar category using fuzzy matching
            if not category:
                best_match = None
                best_score = 0.0
                best_match_type = None

                for cat in all_categories:
                    # Calculate similarity with title
                    title_score = SequenceMatcher(None, filename_without_ext, cat.title).ratio()
                    if title_score > best_score:
                        best_score = title_score
                        best_match = cat
                        best_match_type = "title similarity"

                    # Calculate similarity with slug
                    if cat.slug:
                        slug_score = SequenceMatcher(None, filename_without_ext, cat.slug).ratio()
                        if slug_score > best_score:
                            best_score = slug_score
                            best_match = cat
                            best_match_type = "slug similarity"

                        # Also try with slugified filename
                        filename_slug = slugify(filename_without_ext, allow_unicode=True)
                        slugified_score = SequenceMatcher(None, filename_slug, cat.slug).ratio()
                        if slugified_score > best_score:
                            best_score = slugified_score
                            best_match = cat
                            best_match_type = "slugified similarity"

                # Use the best match if it meets the threshold
                if best_match and best_score >= similarity_threshold:
                    category = best_match
                    match_type = best_match_type
                    similarity_score = best_score

            if not category:
                self.stdout.write(
                    self.style.WARNING(f"   ⚠️  No category found (best match below threshold {similarity_threshold})")
                )
                not_found_count += 1
                continue

            # Found a matching category
            self.stdout.write(
                self.style.SUCCESS(
                    f"   ✓ Found category: {category.title} (ID: {category.id}) "
                    f"[{match_type}, similarity: {similarity_score:.2f}]"
                )
            )

            if dry_run:
                self.stdout.write(f"   [DRY RUN] Would set logo and enable home_page")
                updated_count += 1
            else:
                # Open the file and assign it to the category logo
                # Django will save it to media/category/ automatically (based on upload_to='category')
                with open(image_file, 'rb') as img_file:
                    django_file = File(img_file, name=image_file.name)
                    category.logo.save(image_file.name, django_file, save=False)
                
                # Enable home_page
                category.home_page = True
                
                # Save the category
                category.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f"   ✓ Updated: logo set, home_page enabled")
                )
                updated_count += 1

        # Summary
        self.stdout.write("\n" + "=" * 60)
        if dry_run:
            self.stdout.write(self.style.WARNING("🔍 DRY RUN SUMMARY"))
        else:
            self.stdout.write(self.style.SUCCESS("✅ UPDATE SUMMARY"))
        
        self.stdout.write(f"   Total image files processed: {len(image_files)}")
        self.stdout.write(
            self.style.SUCCESS(f"   Categories updated: {updated_count}")
        )
        if not_found_count > 0:
            self.stdout.write(
                self.style.WARNING(f"   Categories not found: {not_found_count}")
            )

