#!/usr/bin/env python3
import requests

def test_dashboard():
    """Test admin dashboard endpoints"""
    
    # Test main dashboard page
    try:
        print("🌐 Testing admin dashboard...")
        response = requests.get("http://localhost:8080")
        print(f"Dashboard Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Dashboard page loads successfully")
        else:
            print("❌ Dashboard page failed to load")
    except Exception as e:
        print(f"❌ Dashboard error: {e}")
    
    # Test login page
    try:
        print("\n🔑 Testing login page...")
        response = requests.get("http://localhost:8080/login.html")
        print(f"Login Page Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Login page loads successfully")
        else:
            print("❌ Login page failed to load")
    except Exception as e:
        print(f"❌ Login page error: {e}")

if __name__ == "__main__":
    test_dashboard()
