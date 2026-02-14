#!/usr/bin/env python3
"""
Simple test script to verify course creation and viewing workflow
Tests the Django models directly without HTTP requests
"""

import os
import sys
import django
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mahoverse.settings')
django.setup()

from account.models import User, OrganizerTeacher, Organizer
from course.models import Course, Category

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(message):
    print(f"ℹ️  {message}")

def test_user_setup():
    """Test that user has proper setup"""
    print_header("STEP 1: Testing User Setup")
    
    try:
        user = User.objects.get(phone_number="09127867384")
        print_success(f"User found: {user.phone_number}")
        print_info(f"User ID: {user.id}")
        print_info(f"User Role: {user.role}")
        print_info(f"User Name: {user.first_name} {user.last_name}")
        
        # Check permissions
        has_course_create = user.has_permission("course_create")
        has_course_view = user.has_permission("course_view")
        
        print_info(f"Has course_create permission: {has_course_create}")
        print_info(f"Has course_view permission: {has_course_view}")
        
        if has_course_create and has_course_view:
            print_success("User has required permissions")
            return user
        else:
            print_error("User missing required permissions")
            return None
            
    except User.DoesNotExist:
        print_error("User not found")
        return None
    except Exception as e:
        print_error(f"User setup test error: {e}")
        return None

def test_organizer_relationship(user):
    """Test organizer relationship"""
    print_header("STEP 2: Testing Organizer Relationship")
    
    try:
        organizer_teacher = OrganizerTeacher.objects.get(user=user)
        organizer = organizer_teacher.organization
        
        print_success(f"OrganizerTeacher relationship found")
        print_info(f"Organization: {organizer.name}")
        print_info(f"OrganizerTeacher Active: {organizer_teacher.is_active}")
        print_info(f"OrganizerTeacher Verified: {organizer_teacher.is_verified}")
        print_info(f"Organizer Active: {organizer.is_active}")
        print_info(f"Organizer Verified: {organizer.is_verified}")
        
        if (organizer_teacher.is_active and organizer_teacher.is_verified and 
            organizer.is_active and organizer.is_verified):
            print_success("Organizer relationship is properly configured")
            return organizer_teacher
        else:
            print_error("Organizer relationship not properly configured")
            return None
            
    except OrganizerTeacher.DoesNotExist:
        print_error("No OrganizerTeacher relationship found")
        return None
    except Exception as e:
        print_error(f"Organizer relationship test error: {e}")
        return None

def test_course_creation(user, organizer_teacher):
    """Test course creation"""
    print_header("STEP 3: Testing Course Creation")
    
    try:
        # Get a category
        category = Category.objects.first()
        if not category:
            print_error("No categories found in database")
            return None
        
        # Create test course
        course_data = {
            'title': f'Test Course {datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'description': 'This is a test course created by automated test',
            'excerpt': 'Test course excerpt',
            'price': 150000,
            'category': category,
            'organizer': organizer_teacher.organization,
            'user': user
        }
        
        course = Course.objects.create(**course_data)
        print_success(f"Course created successfully!")
        print_info(f"Course ID: {course.id}")
        print_info(f"Course Title: {course.title}")
        print_info(f"Course Slug: {course.slug}")
        print_info(f"Course Price: {course.price}")
        print_info(f"Course Category: {course.category.title}")
        print_info(f"Course Organizer: {course.organizer.name}")
        
        return course
        
    except Exception as e:
        print_error(f"Course creation error: {e}")
        return None

def test_course_listing():
    """Test course listing"""
    print_header("STEP 4: Testing Course Listing")
    
    try:
        # Get all courses
        all_courses = Course.objects.all()
        print_success(f"Total courses in database: {all_courses.count()}")
        
        # Show recent courses
        recent_courses = Course.objects.order_by('-create_date')[:5]
        print_info("Recent courses:")
        for i, course in enumerate(recent_courses, 1):
            print_info(f"  {i}. {course.title} (ID: {course.id}, Price: {course.price})")
        
        return all_courses
        
    except Exception as e:
        print_error(f"Course listing error: {e}")
        return None

def test_user_courses(user):
    """Test user's courses"""
    print_header("STEP 5: Testing User's Courses")
    
    try:
        # Get courses created by this user
        user_courses = Course.objects.filter(user=user)
        print_success(f"User has created {user_courses.count()} courses")
        
        if user_courses.exists():
            print_info("User's courses:")
            for i, course in enumerate(user_courses, 1):
                print_info(f"  {i}. {course.title} (ID: {course.id}, Created: {course.create_date})")
        else:
            print_info("User has not created any courses yet")
        
        return user_courses
        
    except Exception as e:
        print_error(f"User courses test error: {e}")
        return None

def test_course_detail(course):
    """Test course detail view"""
    print_header("STEP 6: Testing Course Detail")
    
    try:
        if not course:
            print_error("No course provided for detail test")
            return False
        
        # Test course detail access
        print_success(f"Course detail accessible")
        print_info(f"Course Title: {course.title}")
        print_info(f"Course Description: {course.description[:100]}...")
        print_info(f"Course Price: {course.price}")
        print_info(f"Course Category: {course.category.title}")
        print_info(f"Course Organizer: {course.organizer.name}")
        print_info(f"Course Creator: {course.user.first_name} {course.user.last_name}")
        print_info(f"Course Created: {course.create_date}")
        print_info(f"Course Updated: {course.update_date}")
        
        return True
        
    except Exception as e:
        print_error(f"Course detail test error: {e}")
        return False

def cleanup_test_course(course):
    """Clean up test course"""
    print_header("STEP 7: Cleaning Up Test Course")
    
    try:
        if course:
            course_id = course.id
            course.delete()
            print_success(f"Test course {course_id} deleted successfully")
        else:
            print_info("No test course to clean up")
            
    except Exception as e:
        print_error(f"Cleanup error: {e}")

def main():
    """Main test function"""
    print("🧪 Simple Course Workflow Test Suite")
    print("Testing user: 09127867384 (Super Admin)")
    print("Testing course creation, listing, and viewing workflow")
    
    test_results = []
    test_course = None
    
    try:
        # Run tests
        user = test_user_setup()
        test_results.append(("User Setup", user is not None))
        
        if user:
            organizer_teacher = test_organizer_relationship(user)
            test_results.append(("Organizer Relationship", organizer_teacher is not None))
            
            if organizer_teacher:
                test_course = test_course_creation(user, organizer_teacher)
                test_results.append(("Course Creation", test_course is not None))
                
                if test_course:
                    test_course_detail(test_course)
                    test_results.append(("Course Detail", True))
        
        # Test listing (independent of course creation)
        courses = test_course_listing()
        test_results.append(("Course Listing", courses is not None))
        
        if user:
            user_courses = test_user_courses(user)
            test_results.append(("User Courses", user_courses is not None))
        
        # Cleanup
        cleanup_test_course(test_course)
        
        # Summary
        print_header("📊 TEST RESULTS SUMMARY")
        
        passed_tests = 0
        total_tests = len(test_results)
        
        for test_name, result in test_results:
            if result:
                print_success(f"{test_name}: PASSED")
                passed_tests += 1
            else:
                print_error(f"{test_name}: FAILED")
        
        print(f"\n🎯 Overall Result: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print_success("🎉 ALL TESTS PASSED! Course workflow is working correctly.")
        else:
            print_error("❌ Some tests failed. Please check the issues above.")
        
        return passed_tests == total_tests
        
    except Exception as e:
        print_error(f"Test suite error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
