#!/usr/bin/env python3
import requests
import json
import time

def comprehensive_test():
    """Comprehensive test to identify the exact error"""
    
    print("🔍 Comprehensive System Diagnostic")
    print("=" * 50)
    
    # Test 1: Check if servers are running
    print("\n1. 🌐 Checking Server Status...")
    
    try:
        response = requests.get("http://localhost:5000/api/auth/login", 
                               json={"username": "admin", "password": "admin123"},
                               timeout=5)
        api_status = "✅ Running" if response.status_code in [200, 405] else "❌ Error"
        print(f"   API Server (5000): {api_status}")
    except:
        print(f"   API Server (5000): ❌ Not responding")
    
    try:
        response = requests.get("http://localhost:8080", timeout=5)
        dashboard_status = "✅ Running" if response.status_code == 200 else "❌ Error"
        print(f"   Dashboard (8080): {dashboard_status}")
    except:
        print(f"   Dashboard (8080): ❌ Not responding")
    
    # Test 2: Login functionality
    print("\n2. 🔑 Testing Login...")
    try:
        login_data = {"username": "admin", "password": "admin123"}
        response = requests.post("http://localhost:5000/api/auth/login", json=login_data, timeout=5)
        
        if response.status_code == 200:
            token = response.json()['access_token']
            print("   ✅ Login successful")
            
            # Test 3: API endpoints with token
            print("\n3. 📡 Testing API Endpoints...")
            headers = {"Authorization": f"Bearer {token}"}
            
            endpoints = [
                ("/api/auth/profile", "User Profile"),
                ("/api/admin/system/stats", "System Stats"),
                ("/api/admin/users", "Users List"),
                ("/api/files/list", "Files List"),
                ("/api/logs/", "Activity Logs")
            ]
            
            for endpoint, name in endpoints:
                try:
                    response = requests.get(f"http://localhost:5000{endpoint}", headers=headers, timeout=5)
                    status = "✅" if response.status_code == 200 else f"❌ ({response.status_code})"
                    print(f"   {status} {name}")
                    if response.status_code != 200:
                        print(f"      Error: {response.text[:100]}...")
                except Exception as e:
                    print(f"   ❌ {name} - Error: {e}")
            
            return token
            
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            print(f"      Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return None

def test_dashboard_flow():
    """Test the complete dashboard flow"""
    print("\n4. 🖥️ Testing Dashboard Flow...")
    
    # Step 1: Get token
    try:
        login_data = {"username": "admin", "password": "admin123"}
        response = requests.post("http://localhost:5000/api/auth/login", json=login_data)
        token = response.json()['access_token']
        
        # Step 2: Simulate dashboard JavaScript calls
        print("   Simulating dashboard JavaScript API calls...")
        
        # These are the exact calls the dashboard makes on load
        calls = [
            ("GET", "http://localhost:5000/api/auth/profile", "Load current user"),
            ("GET", "http://localhost:5000/api/admin/system/stats", "Load system stats"),
            ("GET", "http://localhost:5000/api/admin/users", "Load users"),
        ]
        
        for method, url, description in calls:
            try:
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Origin": "http://localhost:8080"
                }
                
                if method == "GET":
                    response = requests.get(url, headers=headers)
                
                status = "✅" if response.status_code == 200 else f"❌ ({response.status_code})"
                print(f"   {status} {description}")
                
                if response.status_code == 404:
                    print(f"      ❌ NOT FOUND: This is likely the error you're seeing!")
                    print(f"      URL: {url}")
                    print(f"      Response: {response.text}")
                elif response.status_code != 200:
                    print(f"      Error: {response.text[:100]}...")
                    
            except Exception as e:
                print(f"   ❌ {description} - Error: {e}")
        
    except Exception as e:
        print(f"   ❌ Dashboard flow test error: {e}")

def check_browser_issues():
    """Check for common browser issues"""
    print("\n5. 🌍 Browser Issue Check...")
    print("   If you're seeing errors in the browser:")
    print("   1. Press F12 to open Developer Tools")
    print("   2. Go to Console tab to see JavaScript errors")
    print("   3. Go to Network tab to see failed requests")
    print("   4. Clear browser cache and localStorage")
    print("   5. Try hard refresh (Ctrl+F5)")

if __name__ == "__main__":
    token = comprehensive_test()
    if token:
        test_dashboard_flow()
    check_browser_issues()
    
    print("\n" + "=" * 50)
    print("🎯 Diagnosis Complete!")
    print("\nIf you're still seeing errors:")
    print("1. Check the browser console (F12) for specific error messages")
    print("2. Look at the Network tab for failed HTTP requests")
    print("3. Try clearing browser data and logging in fresh")
    print("4. Make sure you're accessing http://localhost:8080")
