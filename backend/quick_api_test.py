#!/usr/bin/env python3
"""
Quick API test to verify HTTP endpoints work correctly
"""

import requests
import json
import time

def test_api_endpoints():
    """Test the API endpoints quickly"""
    base_url = "http://localhost:8000"
    user_phone = "09127867384"
    
    print("🧪 Quick API Test")
    print("=" * 50)
    
    # Step 1: Get OTP
    print("1. Getting OTP...")
    try:
        otp_response = requests.post(f"{base_url}/auth/code/send", 
                                   json={"phone_number": user_phone}, timeout=5)
        if otp_response.status_code == 200:
            otp_data = otp_response.json()
            if otp_data.get('status') and otp_data.get('data', {}).get('code'):
                otp_code = otp_data['data']['code']
                print(f"✅ OTP generated: {otp_code}")
                
                # Step 2: Verify OTP
                print("2. Verifying OTP...")
                verify_response = requests.post(f"{base_url}/auth/code/check",
                                              json={"phone_number": user_phone, "code": otp_code}, timeout=5)
                if verify_response.status_code == 200:
                    verify_data = verify_response.json()
                    if verify_data.get('status'):
                        token = verify_data['data']['token']
                        print("✅ Authentication successful!")
                        
                        headers = {"Authorization": f"Bearer {token}"}
                        
                        # Step 3: Test course creation
                        print("3. Testing course creation...")
                        course_data = {
                            'title': f'API Test Course {int(time.time())}',
                            'description': 'Test course via API',
                            'excerpt': 'API test',
                            'price': '200000',
                            'category': '1'
                        }
                        
                        create_response = requests.post(f"{base_url}/course/create", 
                                                      data=course_data, headers=headers, timeout=10)
                        if create_response.status_code == 200:
                            create_data = create_response.json()
                            if create_data.get('status'):
                                course_id = create_data['data']['id']
                                print(f"✅ Course created successfully! ID: {course_id}")
                                
                                # Step 4: Test course list
                                print("4. Testing course list...")
                                list_data = {
                                    "search": "",
                                    "category_id": None,
                                    "organizer_id": None,
                                    "min_price": None,
                                    "max_price": None,
                                    "ordering": "-create_date"
                                }
                                
                                list_response = requests.post(f"{base_url}/course/list", 
                                                            json=list_data, headers=headers, timeout=5)
                                if list_response.status_code == 200:
                                    list_data = list_response.json()
                                    if list_data.get('status'):
                                        courses = list_data['data']['data']
                                        print(f"✅ Course list retrieved! Found {len(courses)} courses")
                                        
                                        # Check if our course is in the list
                                        course_found = any(course['id'] == course_id for course in courses)
                                        if course_found:
                                            print("✅ Created course found in course list!")
                                        else:
                                            print("❌ Created course not found in course list")
                                        
                                        # Step 5: Test user courses
                                        print("5. Testing user courses...")
                                        user_response = requests.post(f"{base_url}/course/user/list", 
                                                                    json={}, headers=headers, timeout=5)
                                        if user_response.status_code == 200:
                                            user_data = user_response.json()
                                            if user_data.get('status'):
                                                user_role = user_data.get('role')
                                                print(f"✅ User courses retrieved! Role: {user_role}")
                                                
                                                if user_role == "teacher":
                                                    user_courses = user_data['data'].get('results', [])
                                                    print(f"✅ Teacher has {len(user_courses)} courses")
                                                    
                                                    # Check if our course is in user's courses
                                                    user_course_found = any(course['id'] == course_id for course in user_courses)
                                                    if user_course_found:
                                                        print("✅ Created course found in user's course list!")
                                                    else:
                                                        print("❌ Created course not found in user's course list")
                                                
                                                print("\n🎉 ALL API TESTS PASSED!")
                                                return True
                                            else:
                                                print(f"❌ User courses failed: {user_data}")
                                        else:
                                            print(f"❌ User courses request failed: {user_response.status_code}")
                                    else:
                                        print(f"❌ Course list failed: {list_data}")
                                else:
                                    print(f"❌ Course list request failed: {list_response.status_code}")
                            else:
                                print(f"❌ Course creation failed: {create_data}")
                        else:
                            print(f"❌ Course creation request failed: {create_response.status_code}")
                    else:
                        print(f"❌ OTP verification failed: {verify_data}")
                else:
                    print(f"❌ OTP verification request failed: {verify_response.status_code}")
            else:
                print(f"❌ OTP generation failed: {otp_data}")
        else:
            print(f"❌ OTP request failed: {otp_response.status_code}")
    except requests.exceptions.Timeout:
        print("❌ Request timeout - server might not be running")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - server might not be running")
    except Exception as e:
        print(f"❌ API test error: {e}")
    
    return False

if __name__ == "__main__":
    success = test_api_endpoints()
    if success:
        print("\n✅ All API endpoints are working correctly!")
    else:
        print("\n❌ Some API endpoints failed. Check the Django server is running.")
