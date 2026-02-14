import csv
from io import TextIOWrapper
from django.utils.text import slugify
from django.db import transaction
from course.models import Course
from account.models import User, Organizer
from category.models import Category
from standards.models import Standards


class CourseImportService:
    REQUIRED_HEADERS = [
        "title", "excerpt", "description", "price", "user", "category", "organizer"
    ]

    @staticmethod
    @transaction.atomic
    def import_from_csv(uploaded_file):
        """
        Import Course data from a CSV file (UploadedFile or file object).
        Returns a detailed result dictionary.
        """
        # Wrap Django UploadedFile (binary) into text stream
        csv_file = TextIOWrapper(uploaded_file.file, encoding="utf-8")
        reader = csv.DictReader(csv_file)

        # ✅ Validate CSV headers
        headers = [h.strip() for h in reader.fieldnames or []]
        missing_headers = [h for h in CourseImportService.REQUIRED_HEADERS if h not in headers]
        if missing_headers:
            raise ValueError(f"Missing required columns: {', '.join(missing_headers)}")

        imported_count = 0
        updated_count = 0
        skipped_rows = []

        for idx, row in enumerate(reader, start=2):  # start=2 (since row 1 is headers)
            try:
                title = row.get("title", "").strip()
                if not title:
                    raise ValueError("Title is missing")

                # Foreign keys
                try:
                    user = User.objects.get(id=row["user"])
                    category = Category.objects.get(id=row["category"])
                    organizer = Organizer.objects.get(id=row["organizer"])
                except Exception as e:
                    raise ValueError(f"Invalid foreign key: {e}")

                mentor = None
                if row.get("mentor"):
                    try:
                        mentor = User.objects.get(id=row["mentor"])
                    except User.DoesNotExist:
                        print(f"⚠️ Mentor not found for row {idx}")

                standard = None
                if row.get("standard"):
                    try:
                        standard = Standards.objects.get(id=row["standard"])
                    except Standards.DoesNotExist:
                        print(f"⚠️ Standard not found for row {idx}")

                # Create or update
                course, created = Course.objects.update_or_create(
                    title=title,
                    defaults={
                        "excerpt": row["excerpt"],
                        "description": row["description"],
                        "price": int(row["price"]),
                        "discount": int(row["discount"]) if row.get("discount") else None,
                        "user": user,
                        "category": category,
                        "organizer": organizer,
                        "mentor": mentor,
                        "standard": standard,
                        "image": row.get("image") or None,
                        "slug": slugify(title, allow_unicode=True),
                    },
                )

                if created:
                    imported_count += 1
                else:
                    updated_count += 1

            except Exception as e:
                skipped_rows.append({
                    "row": idx,
                    "title": row.get("title"),
                    "error": str(e)
                })
                continue

        return {
            "imported": imported_count,
            "updated": updated_count,
            "skipped": len(skipped_rows),
            "errors": skipped_rows,
        }
