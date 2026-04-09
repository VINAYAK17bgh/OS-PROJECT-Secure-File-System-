#!/usr/bin/env python3
import requests

def check_all_routes():
    """Check all possible routes that might be causing issues"""
    
    print("🗺️ Checking All Routes")
    print("=" * 30)
    
    # Login first
    login_data = {"username": "admin", "password": "admin123"}
    response = requests.post("http://localhost:5000/api/auth/login", json=login_data)
    
    if response.status_code != 200:
        print(f"❌ Cannot login: {response.text}")
        return
    
    token = response.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    
    # Check all routes that might be called
    routes = [
        # Auth routes
        ("GET", "/api/auth/profile"),
        ("POST", "/api/auth/logout"),
        
        # Admin routes
        ("GET", "/api/admin/users"),
        ("GET", "/api/admin/users/1"),
        ("GET", "/api/admin/files"),
        ("GET", "/api/admin/system/stats"),
        ("GET", "/api/admin/security/suspicious-activity"),
        
        # File routes
        ("GET", "/api/files/list"),
        
        # Log routes
        ("GET", "/api/logs/"),
        ("GET", "/api/logs/summary"),
        ("GET", "/api/logs/export"),
        
        # Potentially missing routes
        ("GET", "/api/admin"),
        ("GET", "/api/"),
        ("GET", "/"),
    ]
    
    print(f"\nTesting {len(routes)} routes...")
    
    for method, route in routes:
        try:
            if method == "GET":
                response = requests.get(f"http://localhost:5000{route}", headers=headers)
            elif method == "POST":
                response = requests.post(f"http://localhost:5000{route}", headers=headers)
            
            status_icon = "✅" if response.status_code == 200 else "⚠️" if response.status_code in [401, 405] else "❌"
            print(f"   {status_icon} {method} {route} - {response.status_code}")
            
            if response.status_code == 404:
                print(f"      ❌ NOT FOUND: {response.text}")
            elif response.status_code not in [200, 401, 405]:
                print(f"      ⚠️ Error: {response.text[:100]}...")
                
        except Exception as e:
            print(f"   ❌ {method} {route} - ERROR: {e}")
    
    print(f"\n✅ Route check completed!")

if __name__ == "__main__":
    check_all_routes()
