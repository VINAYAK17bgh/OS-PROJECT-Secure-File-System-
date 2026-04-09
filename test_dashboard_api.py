#!/usr/bin/env python3
import requests

def test_dashboard_api_calls():
    """Test the exact API calls that the dashboard makes"""
    
    print("🔍 Testing Dashboard API Calls")
    print("=" * 40)
    
    # First login to get token
    login_data = {"username": "admin", "password": "admin123"}
    
    try:
        # Login
        response = requests.post("http://localhost:5000/api/auth/login", json=login_data)
        if response.status_code != 200:
            print(f"❌ Login failed: {response.text}")
            return
        
        token = response.json()['access_token']
        headers = {"Authorization": f"Bearer {token}"}
        
        print("✅ Login successful, testing dashboard API calls...")
        
        # Test the exact sequence the dashboard makes
        print("\n1. Testing current user profile...")
        response = requests.get("http://localhost:5000/api/auth/profile", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Profile loaded")
        else:
            print(f"   ❌ Profile failed: {response.text}")
        
        print("\n2. Testing system stats...")
        response = requests.get("http://localhost:5000/api/admin/system/stats", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Stats loaded")
        else:
            print(f"   ❌ Stats failed: {response.text}")
        
        print("\n3. Testing users list...")
        response = requests.get("http://localhost:5000/api/admin/users", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Users loaded")
        else:
            print(f"   ❌ Users failed: {response.text}")
        
        print("\n4. Testing files list...")
        response = requests.get("http://localhost:5000/api/admin/files", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Files loaded")
        else:
            print(f"   ❌ Files failed: {response.text}")
        
        print("\n5. Testing logs...")
        response = requests.get("http://localhost:5000/api/logs/", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Logs loaded")
        else:
            print(f"   ❌ Logs failed: {response.text}")
        
        print("\n6. Testing security data...")
        response = requests.get("http://localhost:5000/api/admin/security/suspicious-activity", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Security data loaded")
        else:
            print(f"   ❌ Security data failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_dashboard_api_calls()
