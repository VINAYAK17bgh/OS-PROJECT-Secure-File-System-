#!/usr/bin/env python3
import requests

def test_cors():
    """Test CORS between dashboard and API"""
    
    # Test if API allows cross-origin requests
    try:
        print("🌐 Testing CORS...")
        
        # Simulate a pre-flight request from the dashboard
        headers = {
            'Origin': 'http://localhost:8080',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type, Authorization'
        }
        
        response = requests.options('http://localhost:5000/api/auth/login', headers=headers)
        
        print(f"CORS Preflight Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ CORS preflight successful")
            print(f"Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'Not set')}")
        else:
            print("❌ CORS preflight failed")
            
    except Exception as e:
        print(f"❌ CORS test error: {e}")
    
    # Test actual login with CORS headers
    try:
        print("\n🔑 Testing login with CORS...")
        headers = {
            'Origin': 'http://localhost:8080',
            'Content-Type': 'application/json'
        }
        
        data = {"username": "admin", "password": "admin123"}
        response = requests.post('http://localhost:5000/api/auth/login', 
                               json=data, headers=headers)
        
        print(f"Login Status: {response.status_code}")
        print(f"CORS Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Login with CORS successful!")
        else:
            print("❌ Login with CORS failed")
            
    except Exception as e:
        print(f"❌ Login test error: {e}")

if __name__ == "__main__":
    test_cors()
