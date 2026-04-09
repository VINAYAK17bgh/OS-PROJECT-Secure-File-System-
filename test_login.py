#!/usr/bin/env python3
import requests
import json

def test_login():
    """Test login functionality"""
    url = "http://localhost:5000/api/auth/login"
    
    # Test admin login
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        print("🔑 Testing admin login...")
        response = requests.post(url, json=login_data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            print(f"Access Token: {data['access_token'][:50]}...")
            return True
        else:
            print("❌ Login failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_register():
    """Test user registration"""
    url = "http://localhost:5000/api/auth/register"
    
    register_data = {
        "username": "testuser",
        "email": "test@example.com", 
        "password": "testpassword123"
    }
    
    try:
        print("\n📝 Testing user registration...")
        response = requests.post(url, json=register_data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
            return True
        else:
            print("❌ Registration failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Secure File System Login")
    print("=" * 40)
    
    # Test admin login first
    admin_login = test_login()
    
    # Test user registration
    test_register()
    
    print("\n" + "=" * 40)
    if admin_login:
        print("✅ Admin login works! You can now:")
        print("   1. Open http://localhost:8080 in your browser")
        print("   2. Login with username: admin, password: admin123")
    else:
        print("❌ There's an issue with the login system")
