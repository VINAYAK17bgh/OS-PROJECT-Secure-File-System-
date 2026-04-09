#!/usr/bin/env python3
import requests

def test_dashboard_to_api():
    """Test if dashboard (port 8080) can reach API (port 5000)"""
    
    print("🌐 Testing Dashboard to API Connection")
    print("=" * 45)
    
    # Test 1: Direct API call (should work)
    print("\n1. Direct API call...")
    try:
        response = requests.get("http://localhost:5000/api/auth/login", 
                               json={"username": "admin", "password": "admin123"})
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Direct API call works")
        else:
            print(f"   ❌ Direct API call failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Direct API call error: {e}")
    
    # Test 2: Simulate CORS preflight from dashboard
    print("\n2. CORS preflight from dashboard...")
    try:
        headers = {
            'Origin': 'http://localhost:8080',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Authorization'
        }
        response = requests.options("http://localhost:5000/api/auth/profile", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ CORS preflight works")
        else:
            print(f"   ❌ CORS preflight failed: {response.text}")
    except Exception as e:
        print(f"   ❌ CORS preflight error: {e}")
    
    # Test 3: Actual call with dashboard origin
    print("\n3. API call with dashboard origin...")
    try:
        # First login
        login_response = requests.post("http://localhost:5000/api/auth/login", 
                                     json={"username": "admin", "password": "admin123"})
        token = login_response.json()['access_token']
        
        # Then call profile with dashboard origin headers
        headers = {
            'Origin': 'http://localhost:8080',
            'Authorization': f'Bearer {token}'
        }
        response = requests.get("http://localhost:5000/api/auth/profile", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ API call with dashboard origin works")
        else:
            print(f"   ❌ API call with dashboard origin failed: {response.text}")
    except Exception as e:
        print(f"   ❌ API call with dashboard origin error: {e}")
    
    # Test 4: Test dashboard accessibility
    print("\n4. Dashboard accessibility...")
    try:
        response = requests.get("http://localhost:8080")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Dashboard accessible")
        else:
            print(f"   ❌ Dashboard not accessible: {response.text}")
    except Exception as e:
        print(f"   ❌ Dashboard error: {e}")

if __name__ == "__main__":
    test_dashboard_to_api()
