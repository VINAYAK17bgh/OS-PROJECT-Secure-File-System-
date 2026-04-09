#!/usr/bin/env python3
import requests
import json

def test_endpoints():
    """Test all API endpoints to find the issue"""
    
    base_url = "http://localhost:5000"
    
    endpoints = [
        "/api/auth/login",
        "/api/auth/profile", 
        "/api/admin/users",
        "/api/admin/system/stats",
        "/api/files/list",
        "/api/logs/"
    ]
    
    print("🔍 Testing API endpoints...")
    print("=" * 50)
    
    # Test login first to get token
    login_data = {"username": "admin", "password": "admin123"}
    
    try:
        print("\n🔑 Testing login...")
        response = requests.post(f"{base_url}/api/auth/login", json=login_data)
        print(f"POST /api/auth/login - Status: {response.status_code}")
        
        if response.status_code == 200:
            token = response.json()['access_token']
            print("✅ Login successful")
            
            # Test other endpoints with token
            headers = {"Authorization": f"Bearer {token}"}
            
            for endpoint in endpoints[1:]:
                try:
                    print(f"\n📡 Testing {endpoint}...")
                    if "admin" in endpoint:
                        response = requests.get(f"{base_url}{endpoint}", headers=headers)
                    elif "files" in endpoint or "logs" in endpoint:
                        response = requests.get(f"{base_url}{endpoint}", headers=headers)
                    else:
                        response = requests.get(f"{base_url}{endpoint}", headers=headers)
                    
                    print(f"GET {endpoint} - Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        print("✅ Success")
                    elif response.status_code == 404:
                        print("❌ Resource not found")
                        print(f"Response: {response.text}")
                    else:
                        print(f"⚠️ Other error: {response.status_code}")
                        print(f"Response: {response.text}")
                        
                except Exception as e:
                    print(f"❌ Error testing {endpoint}: {e}")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Login error: {e}")

def test_routes():
    """Test what routes are actually registered"""
    try:
        print("\n🗺️ Testing available routes...")
        
        # Test root
        response = requests.get("http://localhost:5000/")
        print(f"GET / - Status: {response.status_code}")
        
        # Test API root
        response = requests.get("http://localhost:5000/api/")
        print(f"GET /api/ - Status: {response.status_code}")
        
        # Test invalid endpoint
        response = requests.get("http://localhost:5000/invalid")
        print(f"GET /invalid - Status: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Route testing error: {e}")

if __name__ == "__main__":
    test_endpoints()
    test_routes()
