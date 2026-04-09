#!/usr/bin/env python3
import requests
import json

def create_user(username, email, password):
    """Create a new user via API"""
    
    print(f"👤 Creating user: {username}")
    print("=" * 40)
    
    user_data = {
        "username": username,
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post("http://localhost:5000/api/auth/register", json=user_data)
        
        if response.status_code == 201:
            print("✅ User created successfully!")
            print(f"   Username: {username}")
            print(f"   Email: {email}")
            print(f"   Password: {password}")
            return True
        else:
            print(f"❌ User creation failed: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        return False

def test_user_login(username, password):
    """Test user login"""
    
    print(f"\n🔑 Testing login for: {username}")
    
    login_data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post("http://localhost:5000/api/auth/login", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            print(f"   User Role: {data['user']['role']}")
            print(f"   User ID: {data['user']['id']}")
            return data['access_token']
        else:
            print(f"❌ Login failed: {response.json()}")
            return None
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

if __name__ == "__main__":
    print("🚀 User Creation and Login Tool")
    print("=" * 50)
    
    # Create a sample user
    success = create_user(
        username="john_doe",
        email="john@example.com", 
        password="johnpassword123"
    )
    
    if success:
        # Test login
        token = test_user_login("john_doe", "johnpassword123")
        
        if token:
            print(f"\n🎉 User is ready to use!")
            print(f"   Login credentials: john_doe / johnpassword123")
            print(f"   Access the dashboard: http://localhost:8080/login.html")
    
    print("\n" + "=" * 50)
    print("📋 Available Users:")
    print("   Admin: admin / admin123")
    print("   Test: testuser / testpassword123") 
    print("   New: john_doe / johnpassword123 (if created successfully)")
