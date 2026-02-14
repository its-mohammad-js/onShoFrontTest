#!/usr/bin/env python3
"""
Test script to verify the time_limit functionality for tasks
"""
import requests
import json

# Test data
test_data = {
    "title": "Test Task with Time Limit",
    "description": "This is a test task to verify time limit functionality",
    "course_id": "1",  # Assuming course with ID 1 exists
    "difficulty": "beginner",
    "time_limit": "30"  # 30 minutes time limit
}

# API endpoint
url = "http://127.0.0.1:8001/course/task/create"

# Headers (you'll need to replace with a valid token)
headers = {
    "Authorization": "Bearer YOUR_TOKEN_HERE",
    "Content-Type": "application/json"
}

def test_time_limit_api():
    """Test the time limit API functionality"""
    print("Testing time limit functionality...")
    
    try:
        # Convert to form data for multipart/form-data
        files = {}
        data = test_data.copy()
        
        response = requests.post(url, data=data, files=files, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Task created successfully with time limit!")
            response_data = response.json()
            if 'data' in response_data and 'time_limit' in response_data['data']:
                print(f"✅ Time limit field included in response: {response_data['data']['time_limit']}")
            else:
                print("❌ Time limit field not found in response")
        else:
            print("❌ Task creation failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Time Limit Test Script")
    print("=" * 50)
    print("Note: Make sure to:")
    print("1. Start the Django server: python3 manage.py runserver")
    print("2. Replace YOUR_TOKEN_HERE with a valid JWT token")
    print("3. Ensure course with ID 1 exists")
    print("=" * 50)
    test_time_limit_api()
