#!/usr/bin/env python
"""
Script to clear all data from the database
This will delete all records from all models while respecting foreign key constraints
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mahoverse.settings')
django.setup()

from django.db import transaction
from django.core.management import call_command

from account.models import (
    UserOtp, OrganizerTeacher, Organizer, User, RolePermission, Permission, Role,
    Zone, City, Province
)
from course.models import (
    TaskAnswer, Task, File, Lesson, Chapter, CourseAttribute, CategoryAttribute,
    AttributeValue, Attribute, Session, Step, Comment, WishList, Rate,
    Course, Category
)
from payment.models import Transaction, CourseOrder, Order, Situation, Status
from ticket.models import Message, Chat
from webinar.models import WebinarTopic, Webinar
from static_content.models import RelatedLink, StaticContent


def clear_all_data():
    """Clear all data from all models in the correct order"""
    print("🗑️  Clearing all data from database...")
    print("=" * 60)
    
    try:
        with transaction.atomic():
            # Delete in reverse order of dependencies
            
            # 1. Delete data that has foreign keys to other models first
            print("Deleting TaskAnswer...")
            TaskAnswer.objects.all().delete()
            print(f"  ✅ Deleted {TaskAnswer.objects.count()} task answers")
            
            print("Deleting Task...")
            Task.objects.all().delete()
            print(f"  ✅ Deleted {Task.objects.count()} tasks")
            
            print("Deleting File...")
            File.objects.all().delete()
            print(f"  ✅ Deleted {File.objects.count()} files")
            
            print("Deleting Lesson...")
            Lesson.objects.all().delete()
            print(f"  ✅ Deleted {Lesson.objects.count()} lessons")
            
            print("Deleting Chapter...")
            Chapter.objects.all().delete()
            print(f"  ✅ Deleted {Chapter.objects.count()} chapters")
            
            print("Deleting CourseAttribute...")
            CourseAttribute.objects.all().delete()
            print(f"  ✅ Deleted {CourseAttribute.objects.count()} course attributes")
            
            print("Deleting CategoryAttribute...")
            CategoryAttribute.objects.all().delete()
            print(f"  ✅ Deleted {CategoryAttribute.objects.count()} category attributes")
            
            print("Deleting AttributeValue...")
            AttributeValue.objects.all().delete()
            print(f"  ✅ Deleted {AttributeValue.objects.count()} attribute values")
            
            print("Deleting Attribute...")
            Attribute.objects.all().delete()
            print(f"  ✅ Deleted {Attribute.objects.count()} attributes")
            
            print("Deleting Session...")
            Session.objects.all().delete()
            print(f"  ✅ Deleted {Session.objects.count()} sessions")
            
            print("Deleting Step...")
            Step.objects.all().delete()
            print(f"  ✅ Deleted {Step.objects.count()} steps")
            
            print("Deleting Comment...")
            Comment.objects.all().delete()
            print(f"  ✅ Deleted {Comment.objects.count()} comments")
            
            print("Deleting WishList...")
            WishList.objects.all().delete()
            print(f"  ✅ Deleted {WishList.objects.count()} wishlist items")
            
            print("Deleting Rate...")
            Rate.objects.all().delete()
            print(f"  ✅ Deleted {Rate.objects.count()} rates")
            
            print("Deleting Course...")
            Course.objects.all().delete()
            print(f"  ✅ Deleted {Course.objects.count()} courses")
            
            print("Deleting Category...")
            Category.objects.all().delete()
            print(f"  ✅ Deleted {Category.objects.count()} categories")
            
            print("Deleting Transaction...")
            Transaction.objects.all().delete()
            print(f"  ✅ Deleted {Transaction.objects.count()} transactions")
            
            print("Deleting CourseOrder...")
            CourseOrder.objects.all().delete()
            print(f"  ✅ Deleted {CourseOrder.objects.count()} course orders")
            
            print("Deleting Order...")
            Order.objects.all().delete()
            print(f"  ✅ Deleted {Order.objects.count()} orders")
            
            print("Deleting Situation...")
            Situation.objects.all().delete()
            print(f"  ✅ Deleted {Situation.objects.count()} situations")
            
            print("Deleting Status...")
            Status.objects.all().delete()
            print(f"  ✅ Deleted {Status.objects.count()} statuses")
            
            print("Deleting Message...")
            Message.objects.all().delete()
            print(f"  ✅ Deleted {Message.objects.count()} messages")
            
            print("Deleting Chat...")
            Chat.objects.all().delete()
            print(f"  ✅ Deleted {Chat.objects.count()} chats")
            
            print("Deleting WebinarTopic...")
            WebinarTopic.objects.all().delete()
            print(f"  ✅ Deleted {WebinarTopic.objects.count()} webinar topics")
            
            print("Deleting Webinar...")
            Webinar.objects.all().delete()
            print(f"  ✅ Deleted {Webinar.objects.count()} webinars")
            
            print("Deleting RelatedLink...")
            RelatedLink.objects.all().delete()
            print(f"  ✅ Deleted {RelatedLink.objects.count()} related links")
            
            print("Deleting StaticContent...")
            StaticContent.objects.all().delete()
            print(f"  ✅ Deleted {StaticContent.objects.count()} static contents")
            
            print("Deleting UserOtp...")
            UserOtp.objects.all().delete()
            print(f"  ✅ Deleted {UserOtp.objects.count()} user OTPs")
            
            print("Deleting OrganizerTeacher...")
            OrganizerTeacher.objects.all().delete()
            print(f"  ✅ Deleted {OrganizerTeacher.objects.count()} organizer teachers")
            
            print("Deleting Organizer...")
            Organizer.objects.all().delete()
            print(f"  ✅ Deleted {Organizer.objects.count()} organizers")
            
            print("Deleting RolePermission...")
            RolePermission.objects.all().delete()
            print(f"  ✅ Deleted {RolePermission.objects.count()} role permissions")
            
            print("Deleting Permission...")
            Permission.objects.all().delete()
            print(f"  ✅ Deleted {Permission.objects.count()} permissions")
            
            print("Deleting Role...")
            Role.objects.all().delete()
            print(f"  ✅ Deleted {Role.objects.count()} roles")
            
            print("Deleting Zone...")
            Zone.objects.all().delete()
            print(f"  ✅ Deleted {Zone.objects.count()} zones")
            
            print("Deleting City...")
            City.objects.all().delete()
            print(f"  ✅ Deleted {City.objects.count()} cities")
            
            print("Deleting Province...")
            Province.objects.all().delete()
            print(f"  ✅ Deleted {Province.objects.count()} provinces")
            
            # Delete users last (they might be referenced by other models)
            print("Deleting User...")
            # Don't delete superuser accounts
            User.objects.filter(is_superuser=False).delete()
            print(f"  ✅ Deleted non-superuser users. Remaining: {User.objects.count()} users")
            
        print("=" * 60)
        print("✅ All data cleared successfully!")
        
    except Exception as e:
        print("=" * 60)
        print(f"❌ Error clearing data: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == '__main__':
    print("🚀 Starting data cleanup...")
    print()
    
    try:
        clear_all_data()
        print()
        print("🎉 Database is now clean and ready for fresh seed data!")
        print("💡 You can now run: python seed_data.py")
        
    except Exception as e:
        print()
        print(f"❌ Failed to clear data: {e}")
        sys.exit(1)

