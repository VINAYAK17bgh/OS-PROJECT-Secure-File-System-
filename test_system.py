#!/usr/bin/env python3
"""
Test script for the Mini Secure File System
This script tests basic functionality of the secure file system.
"""

import requests
import json
import os
import time

# Configuration
BASE_URL = "http://localhost:5000"
ADMIN_DASHBOARD_URL = "http://localhost:8080"

def test_api_connection():
    """Test if the API server is running"""
    try:
        response = requests.get(f"{BASE_URL}/api/auth/profile")
        return False  # Should return 401 without auth
    except requests.exceptions.ConnectionError:
        print("❌ API server is not running on port 5000")
        return False
    except:
        return True  # Got 401, which means server is running

def test_admin_dashboard():
    """Test if the admin dashboard is running"""
    try:
        response = requests.get(ADMIN_DASHBOARD_URL)
        if response.status_code == 200:
            print("✅ Admin dashboard is running")
            return True
        else:
            print("❌ Admin dashboard returned unexpected status")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Admin dashboard is not running on port 8080")
        return False

def test_user_registration():
    """Test user registration"""
    print("\n📝 Testing user registration...")
    
    test_user = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=test_user
        )
        
        if response.status_code == 201:
            print("✅ User registration successful")
            return True
        else:
            print(f"❌ Registration failed: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False

def test_user_login():
    """Test user login"""
    print("\n🔑 Testing user login...")
    
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ User login successful")
            return data['access_token']
        else:
            print(f"❌ Login failed: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_file_upload(token):
    """Test file upload"""
    print("\n📁 Testing file upload...")
    
    # Create a test file
    test_content = b"This is a test file for the secure file system."
    
    try:
        files = {'file': ('test.txt', test_content, 'text/plain')}
        data = {'is_public': 'false'}
        headers = {'Authorization': f'Bearer {token}'}
        
        response = requests.post(
            f"{BASE_URL}/api/files/upload",
            files=files,
            data=data,
            headers=headers
        )
        
        if response.status_code == 201:
            file_data = response.json()
            print("✅ File upload successful")
            return file_data['file']['id']
        else:
            print(f"❌ File upload failed: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ File upload error: {e}")
        return None

def test_file_list(token):
    """Test file listing"""
    print("\n📋 Testing file listing...")
    
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(
            f"{BASE_URL}/api/files/list",
            headers=headers
        )
        
        if response.status_code == 200:
            files = response.json()['files']
            print(f"✅ File listing successful. Found {len(files)} files")
            return files
        else:
            print(f"❌ File listing failed: {response.json()}")
            return []
    except Exception as e:
        print(f"❌ File listing error: {e}")
        return []

def test_admin_login():
    """Test admin login"""
    print("\n👑 Testing admin login...")
    
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Admin login successful")
            return data['access_token']
        else:
            print(f"❌ Admin login failed: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Admin login error: {e}")
        return None

def test_admin_stats(token):
    """Test admin statistics"""
    print("\n📊 Testing admin statistics...")
    
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(
            f"{BASE_URL}/api/admin/system/stats",
            headers=headers
        )
        
        if response.status_code == 200:
            stats = response.json()
            print("✅ Admin statistics successful")
            print(f"   - Total users: {stats['users']['total']}")
            print(f"   - Total files: {stats['files']['total']}")
            print(f"   - Storage used: {stats['files']['total_storage_mb']} MB")
            return True
        else:
            print(f"❌ Admin statistics failed: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Admin statistics error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Mini Secure File System Tests")
    print("=" * 50)
    
    # Test server connections
    api_ok = test_api_connection()
    dashboard_ok = test_admin_dashboard()
    
    if not api_ok:
        print("\n❌ Please start the API server first: python run.py")
        return
    
    if not dashboard_ok:
        print("\n❌ Please start the admin dashboard first: python admin_dashboard.py")
        return
    
    # Test user functionality
    registration_ok = test_user_registration()
    if not registration_ok:
        print("\n❌ User registration failed, stopping tests")
        return
    
    user_token = test_user_login()
    if not user_token:
        print("\n❌ User login failed, stopping tests")
        return
    
    file_id = test_file_upload(user_token)
    files = test_file_list(user_token)
    
    # Test admin functionality
    admin_token = test_admin_login()
    if admin_token:
        test_admin_stats(admin_token)
    else:
        print("\n⚠️ Admin login failed, skipping admin tests")
    
    print("\n" + "=" * 50)
    print("✅ All available tests completed!")
    print("\n📖 Next steps:")
    print("1. Open your browser and go to: http://localhost:8080")
    print("2. Login with admin/admin123")
    print("3. Explore the admin dashboard")
    print("4. Try uploading and managing files through the API")

if __name__ == "__main__":
    main()
