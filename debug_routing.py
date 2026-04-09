#!/usr/bin/env python3
import requests

def find_broken_route():
    """Find which URL is causing the routing error"""
    
    print("🔍 Finding the Broken Route")
    print("=" * 35)
    
    # Test common URLs that might be causing issues
    test_urls = [
        "http://localhost:5000/",
        "http://localhost:5000/api",
        "http://localhost:5000/api/",
        "http://localhost:5000/api/admin",
        "http://localhost:5000/api/auth",
        "http://localhost:5000/api/files",
        "http://localhost:5000/api/logs",
        "http://localhost:8080/",
        "http://localhost:8080/api",
        "http://localhost:8080/api/",
    ]
    
    print("Testing common URLs that might cause routing errors...")
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=3)
            status = "✅" if response.status_code == 200 else f"❌ ({response.status_code})"
            print(f"   {status} {url}")
            
            if response.status_code == 404:
                print(f"      ❌ This URL causes 404 - likely the problem!")
                print(f"      Response: {response.text}")
                
        except Exception as e:
            print(f"   ❌ {url} - Error: {e}")
    
    # Test with authentication to see if protected routes cause issues
    print("\nTesting authenticated routes...")
    
    try:
        # Login first
        login_response = requests.post("http://localhost:5000/api/auth/login", 
                                     json={"username": "admin", "password": "admin123"})
        
        if login_response.status_code == 200:
            token = login_response.json()['access_token']
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test some potentially problematic URLs
            auth_urls = [
                "http://localhost:5000/api/admin",
                "http://localhost:5000/api/",
                "http://localhost:5000/api",
            ]
            
            for url in auth_urls:
                try:
                    response = requests.get(url, headers=headers, timeout=3)
                    status = "✅" if response.status_code == 200 else f"❌ ({response.status_code})"
                    print(f"   {status} {url} (authenticated)")
                    
                    if response.status_code == 404:
                        print(f"      ❌ Authenticated 404 - this might be the issue!")
                        print(f"      Response: {response.text}")
                        
                except Exception as e:
                    print(f"   ❌ {url} (authenticated) - Error: {e}")
        
    except Exception as e:
        print(f"❌ Could not test authenticated routes: {e}")

if __name__ == "__main__":
    find_broken_route()
