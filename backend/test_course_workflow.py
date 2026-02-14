#!/usr/bin/env python3
"""
Comprehensive test script to verify course creation and viewing workflow
for user 09127867384 (Super Admin)
"""

import os
import sys
import django
import requests
import json
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mahoverse.settings')
django.setup()

from account.models import User, OrganizerTeacher, Organizer
from course.models import Course

class CourseWorkflowTester:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.user_phone = "09127867384"
        self.token = None
        self.test_course_id = None
        
    def print_header(self, title):
        print(f"\n{'='*60}")
        print(f"🧪 {title}")
        print(f"{'='*60}")
    
    def print_success(self, message):
        print(f"✅ {message}")
    
    def print_error(self, message):
        print(f"❌ {message}")
    
    def print_info(self, message):
        print(f"ℹ️  {message}")
    
    def get_auth_token(self):
        """Get authentication token for the user"""
        self.print_header("STEP 1: Getting Authentication Token")
        
        try:
            # First, send OTP
            otp_response = requests.post(f"{self.base_url}/auth/code/send", 
                                       json={"phone_number": self.user_phone})
            
            if otp_response.status_code == 200:
                otp_data = otp_response.json()
                if otp_data.get('status') and otp_data.get('data', {}).get('code'):
                    otp_code = otp_data['data']['code']
                    self.print_success(f"OTP generated: {otp_code}")
                    
                    # Verify OTP and get token
                    verify_response = requests.post(f"{self.base_url}/auth/code/check",
                                                  json={"phone_number": self.user_phone, "code": otp_code})
                    
                    if verify_response.status_code == 200:
                        verify_data = verify_response.json()
                        if verify_data.get('status'):
                            self.token = verify_data['data']['token']
                            self.print_success("Authentication successful!")
                            return True
                        else:
                            self.print_error(f"OTP verification failed: {verify_data}")
                    else:
                        self.print_error(f"OTP verification request failed: {verify_response.status_code}")
                else:
                    self.print_error(f"OTP generation failed: {otp_data}")
            else:
                self.print_error(f"OTP request failed: {otp_response.status_code}")
                
        except Exception as e:
            self.print_error(f"Authentication error: {e}")
        
        return False
    
    def test_user_permissions(self):
        """Test that user has required permissions"""
        self.print_header("STEP 2: Verifying User Permissions")
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(f"{self.base_url}/auth/permissions/user", 
                                   json={}, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status'):
                    permissions = [p['slug'] for p in data['data']]
                    
                    required_permissions = ['course_create', 'course_view']
                    missing_permissions = [p for p in required_permissions if p not in permissions]
                    
                    if not missing_permissions:
                        self.print_success("User has all required permissions")
                        self.print_info(f"Permissions: {', '.join(permissions)}")
                        return True
                    else:
                        self.print_error(f"Missing permissions: {missing_permissions}")
                else:
                    self.print_error(f"Permission check failed: {data}")
            else:
                self.print_error(f"Permission request failed: {response.status_code}")
                
        except Exception as e:
            self.print_error(f"Permission check error: {e}")
        
        return False
    
    def test_organizer_relationship(self):
        """Test that user has proper organizer relationship"""
        self.print_header("STEP 3: Verifying Organizer Relationship")
        
        try:
            user = User.objects.get(phone_number=self.user_phone)
            organizer_teacher = OrganizerTeacher.objects.get(user=user)
            
            self.print_success(f"User: {user.phone_number}")
            self.print_success(f"Organization: {organizer_teacher.organization.name}")
            self.print_success(f"OrganizerTeacher Active: {organizer_teacher.is_active}")
            self.print_success(f"OrganizerTeacher Verified: {organizer_teacher.is_verified}")
            self.print_success(f"Organizer Active: {organizer_teacher.organization.is_active}")
            self.print_success(f"Organizer Verified: {organizer_teacher.organization.is_verified}")
            
            return True
            
        except OrganizerTeacher.DoesNotExist:
            self.print_error("No OrganizerTeacher relationship found")
            return False
        except Exception as e:
            self.print_error(f"Organizer relationship check error: {e}")
            return False
    
    def test_course_creation(self):
        """Test course creation"""
        self.print_header("STEP 4: Testing Course Creation")
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            
            # Create test course data
            course_data = {
                'title': f'Test Course {datetime.now().strftime("%Y%m%d_%H%M%S")}',
                'description': 'This is a test course created by automated test',
                'excerpt': 'Test course excerpt',
                'price': '150000',
                'category': '1'
            }
            
            response = requests.post(f"{self.base_url}/course/create", 
                                   data=course_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status'):
                    course_info = data['data']
                    self.test_course_id = course_info['id']
                    self.print_success(f"Course created successfully!")
                    self.print_info(f"Course ID: {course_info['id']}")
                    self.print_info(f"Course Title: {course_info['title']}")
                    self.print_info(f"Course Slug: {course_info['slug']}")
                    self.print_info(f"Course Price: {course_info['price']}")
                    return True
                else:
                    self.print_error(f"Course creation failed: {data}")
            else:
                self.print_error(f"Course creation request failed: {response.status_code}")
                self.print_error(f"Response: {response.text}")
                
        except Exception as e:
            self.print_error(f"Course creation error: {e}")
        
        return False
    
    def test_course_list_view(self):
        """Test viewing courses in the main course list"""
        self.print_header("STEP 5: Testing Course List View")
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            
            list_data = {
                "search": "",
                "category_id": None,
                "organizer_id": None,
                "min_price": None,
                "max_price": None,
                "ordering": "-create_date"
            }
            
            response = requests.post(f"{self.base_url}/course/list", 
                                   json=list_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status'):
                    courses = data['data']['data']
                    self.print_success(f"Course list retrieved successfully!")
                    self.print_info(f"Total courses found: {len(courses)}")
                    
                    # Check if our test course is in the list
                    test_course_found = any(course['id'] == self.test_course_id for course in courses)
                    if test_course_found:
                        self.print_success("Test course found in course list!")
                    else:
                        self.print_error("Test course not found in course list")
                    
                    # Show first few courses
                    for i, course in enumerate(courses[:3]):
                        self.print_info(f"Course {i+1}: {course['title']} (ID: {course['id']})")
                    
                    return True
                else:
                    self.print_error(f"Course list retrieval failed: {data}")
            else:
                self.print_error(f"Course list request failed: {response.status_code}")
                
        except Exception as e:
            self.print_error(f"Course list error: {e}")
        
        return False
    
    def test_user_courses_view(self):
        """Test viewing user's own courses"""
        self.print_header("STEP 6: Testing User Courses View")
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            
            response = requests.post(f"{self.base_url}/course/user/list", 
                                   json={}, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status'):
                    user_role = data.get('role')
                    courses_data = data['data']
                    
                    self.print_success(f"User courses retrieved successfully!")
                    self.print_info(f"User role: {user_role}")
                    
                    if user_role == "teacher":
                        courses = courses_data.get('results', [])
                        self.print_info(f"Teacher courses found: {len(courses)}")
                        
                        # Check if our test course is in user's courses
                        test_course_found = any(course['id'] == self.test_course_id for course in courses)
                        if test_course_found:
                            self.print_success("Test course found in user's course list!")
                        else:
                            self.print_error("Test course not found in user's course list")
                        
                        # Show user's courses
                        for i, course in enumerate(courses):
                            self.print_info(f"User Course {i+1}: {course['title']} (ID: {course['id']})")
                    
                    return True
                else:
                    self.print_error(f"User courses retrieval failed: {data}")
            else:
                self.print_error(f"User courses request failed: {response.status_code}")
                
        except Exception as e:
            self.print_error(f"User courses error: {e}")
        
        return False
    
    def test_course_detail_view(self):
        """Test viewing course detail"""
        self.print_header("STEP 7: Testing Course Detail View")
        
        if not self.test_course_id:
            self.print_error("No test course ID available")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            
            # Get course slug from database
            course = Course.objects.get(id=self.test_course_id)
            
            detail_data = {"slug": course.slug}
            
            response = requests.post(f"{self.base_url}/course/detail", 
                                   json=detail_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status'):
                    course_info = data['data']
                    self.print_success(f"Course detail retrieved successfully!")
                    self.print_info(f"Course Title: {course_info['title']}")
                    self.print_info(f"Course Description: {course_info['description'][:100]}...")
                    self.print_info(f"Course Price: {course_info['price']}")
                    self.print_info(f"Course Organizer: {course_info.get('organizer', {}).get('name', 'N/A')}")
                    return True
                else:
                    self.print_error(f"Course detail retrieval failed: {data}")
            else:
                self.print_error(f"Course detail request failed: {response.status_code}")
                
        except Exception as e:
            self.print_error(f"Course detail error: {e}")
        
        return False
    
    def cleanup_test_course(self):
        """Clean up the test course"""
        self.print_header("STEP 8: Cleaning Up Test Course")
        
        if self.test_course_id:
            try:
                course = Course.objects.get(id=self.test_course_id)
                course.delete()
                self.print_success(f"Test course {self.test_course_id} deleted successfully")
            except Exception as e:
                self.print_error(f"Failed to delete test course: {e}")
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        self.print_header("🚀 STARTING COMPREHENSIVE COURSE WORKFLOW TEST")
        
        test_results = []
        
        # Run all tests
        test_results.append(("Authentication", self.get_auth_token()))
        test_results.append(("User Permissions", self.test_user_permissions()))
        test_results.append(("Organizer Relationship", self.test_organizer_relationship()))
        test_results.append(("Course Creation", self.test_course_creation()))
        test_results.append(("Course List View", self.test_course_list_view()))
        test_results.append(("User Courses View", self.test_user_courses_view()))
        test_results.append(("Course Detail View", self.test_course_detail_view()))
        
        # Cleanup
        self.cleanup_test_course()
        
        # Summary
        self.print_header("📊 TEST RESULTS SUMMARY")
        
        passed_tests = 0
        total_tests = len(test_results)
        
        for test_name, result in test_results:
            if result:
                self.print_success(f"{test_name}: PASSED")
                passed_tests += 1
            else:
                self.print_error(f"{test_name}: FAILED")
        
        print(f"\n🎯 Overall Result: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            self.print_success("🎉 ALL TESTS PASSED! Course workflow is working correctly.")
        else:
            self.print_error("❌ Some tests failed. Please check the issues above.")
        
        return passed_tests == total_tests

def main():
    """Main function to run the tests"""
    print("🧪 Course Workflow Test Suite")
    print("Testing user: 09127867384 (Super Admin)")
    print("Testing course creation, listing, and viewing workflow")
    
    tester = CourseWorkflowTester()
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
