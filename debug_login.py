#!/usr/bin/env python3
import requests
import json

def debug_login_issue():
    """Debug the login issue"""
    
    print("🔍 Debugging Login Issue")
    print("=" * 30)
    
    # Test all known users
    users = [
        {"username": "admin", "password": "admin123"},
        {"username": "testuser", "password": "testpassword123"},
        {"username": "john_doe", "password": "johnpassword123"}
    ]
    
    for user in users:
        print(f"\n👤 Testing user: {user['username']}")
        
        try:
            response = requests.post("http://localhost:5000/api/auth/login", json=user)
            
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
            
            if response.status_code == 200:
                print("   ✅ Login successful!")
                data = response.json()
                print(f"   User ID: {data['user']['id']}")
                print(f"   Role: {data['user']['role']}")
                print(f"   Email: {data['user']['email']}")
            else:
                print("   ❌ Login failed")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Check what users actually exist in the database
    print(f"\n🗄️ Checking existing users...")
    
    try:
        # Login as admin to get user list
        admin_response = requests.post("http://localhost:5000/api/auth/login", 
                                     json={"username": "admin", "password": "admin123"})
        
        if admin_response.status_code == 200:
            token = admin_response.json()['access_token']
            headers = {"Authorization": f"Bearer {token}"}
            
            # Get all users
            users_response = requests.get("http://localhost:5000/api/admin/users", headers=headers)
            
            if users_response.status_code == 200:
                users = users_response.json()['users']
                print(f"   Found {len(users)} users in database:")
                for user in users:
                    print(f"   - ID: {user['id']}, Username: {user['username']}, Email: {user['email']}, Role: {user['role']}, Active: {user['is_active']}")
            else:
                print(f"   ❌ Could not get user list: {users_response.text}")
        else:
            print(f"   ❌ Admin login failed: {admin_response.text}")
            
    except Exception as e:
        print(f"   ❌ Error checking users: {e}")

def test_password_reset():
    """Test if we can reset or recreate users"""
    
    print(f"\n🔄 Testing user recreation...")
    
    # Try to create a simple test user
    test_user = {
        "username": "test_user_new",
        "email": "test@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post("http://localhost:5000/api/auth/register", json=test_user)
        
        if response.status_code == 201:
            print("   ✅ New test user created successfully!")
            print(f"   Username: test_user_new")
            print(f"   Password: password123")
            
            # Test login immediately
            login_response = requests.post("http://localhost:5000/api/auth/login", 
                                         json={"username": "test_user_new", "password": "password123"})
            
            if login_response.status_code == 200:
                print("   ✅ New user login works!")
            else:
                print(f"   ❌ New user login failed: {login_response.text}")
        else:
            print(f"   ❌ User creation failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error creating user: {e}")

if __name__ == "__main__":
    debug_login_issue()
    test_password_reset()
    
    print(f"\n" + "=" * 50)
    print("🎯 Quick Fix Options:")
    print("1. Use the newly created test_user_new / password123")
    print("2. Try admin / admin123 (should work)")
    print("3. Clear browser cache and localStorage")
    print("4. Make sure you're using the correct login page: http://localhost:8080/login.html")
