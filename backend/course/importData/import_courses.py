import csv
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from course.models import Course
from account.models import User, Organizer
from category.models import Category
from standards.models import Standards


class Command(BaseCommand):
    help = "Import courses from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file")

    def handle(self, *args, **options):
        csv_file_path = options["csv_file"]

        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    title = row["title"].strip()

                    # Foreign keys
                    try:
                        user = User.objects.get(id=row["user"])
                        category = Category.objects.get(id=row["category"])
                        organizer = Organizer.objects.get(id=row["organizer"])
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Skipping '{title}': foreign key missing → {e}"))
                        continue

                    mentor = None
                    if row.get("mentor"):
                        try:
                            mentor = User.objects.get(id=row["mentor"])
                        except User.DoesNotExist:
                            self.stdout.write(self.style.WARNING(f"Mentor with id {row['mentor']} not found."))

                    standard = None
                    if row.get("standard"):
                        try:
                            standard = Standards.objects.get(id=row["standard"])
                        except Standards.DoesNotExist:
                            self.stdout.write(self.style.WARNING(f"Standard with id {row['standard']} not found."))

                    # Create or update course
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
                            "image": row["image"] if row.get("image") else None,
                            "slug": slugify(title, allow_unicode=True)
                        },
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Created course: {course.title}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Updated existing course: {course.title}"))

        except FileNotFoundError:
            raise CommandError(f"File not found: {csv_file_path}")
        except Exception as e:
            raise CommandError(f"Error importing data: {e}")
