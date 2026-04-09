#!/usr/bin/env python3
import requests
import json

def debug_network_connection():
    """Debug network connection between dashboard and API"""
    
    print("🌐 Network Connection Debug")
    print("=" * 35)
    
    # Test 1: Check if API server is running
    print("\n1. 🔍 Testing API Server Connection...")
    try:
        response = requests.get("http://localhost:5000/api/auth/login", timeout=5)
        print(f"   ✅ API Server (5000): Responding with status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ API Server (5000): Connection refused - not running?")
        return
    except requests.exceptions.Timeout:
        print("   ❌ API Server (5000): Timeout - server slow or not responding")
        return
    except Exception as e:
        print(f"   ❌ API Server (5000): Error - {e}")
        return
    
    # Test 2: Check if dashboard server is running
    print("\n2. 🔍 Testing Dashboard Server Connection...")
    try:
        response = requests.get("http://localhost:8080/", timeout=5)
        print(f"   ✅ Dashboard Server (8080): Responding with status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Dashboard Server (8080): Connection refused - not running?")
        return
    except requests.exceptions.Timeout:
        print("   ❌ Dashboard Server (8080): Timeout - server slow or not responding")
        return
    except Exception as e:
        print(f"   ❌ Dashboard Server (8080): Error - {e}")
        return
    
    # Test 3: Test login to get a valid token
    print("\n3. 🔑 Testing Authentication...")
    try:
        login_data = {"username": "testuser", "password": "testpassword123"}
        response = requests.post("http://localhost:5000/api/auth/login", json=login_data, timeout=5)
        
        if response.status_code == 200:
            token = response.json()['access_token']
            print("   ✅ Authentication successful")
            
            # Test 4: Test file upload endpoint
            print("\n4. 📤 Testing File Upload Endpoint...")
            
            # Create a test file
            test_content = b"This is a test file for network debugging."
            files = {'file': ('test.txt', test_content, 'text/plain')}
            data = {'is_public': 'false'}
            headers = {'Authorization': f'Bearer {token}'}
            
            try:
                response = requests.post(
                    "http://localhost:5000/api/files/upload",
                    files=files,
                    data=data,
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 201:
                    print("   ✅ File upload endpoint working")
                    file_data = response.json()['file']
                    print(f"      File ID: {file_data['id']}")
                    
                    # Test 5: Test file listing
                    print("\n5. 📋 Testing File Listing...")
                    response = requests.get("http://localhost:5000/api/files/list", headers=headers, timeout=5)
                    
                    if response.status_code == 200:
                        files = response.json()['files']
                        print(f"   ✅ File listing working - Found {len(files)} files")
                        
                        if files:
                            print("   📁 Your uploaded files:")
                            for file in files:
                                print(f"      - {file['original_filename']} ({file['file_size']} bytes)")
                                print(f"        Uploaded: {file['created_at']}")
                                print(f"        Public: {'Yes' if file['is_public'] else 'No'}")
                                print(f"        File ID: {file['id']}")
                                print()
                    else:
                        print(f"   ❌ File listing failed: {response.status_code}")
                        
                else:
                    print(f"   ❌ File upload failed: {response.status_code}")
                    print(f"      Error: {response.text}")
                    
            except requests.exceptions.Timeout:
                print("   ❌ File upload timeout - might be a large file or slow server")
            except Exception as e:
                print(f"   ❌ File upload error: {e}")
                
        else:
            print(f"   ❌ Authentication failed: {response.status_code}")
            print(f"      Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Authentication error: {e}")

def check_cors():
    """Check CORS configuration"""
    print("\n6. 🌍 Testing CORS Configuration...")
    
    try:
        # Test preflight request
        response = requests.options(
            "http://localhost:5000/api/files/upload",
            headers={
                'Origin': 'http://localhost:8080',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Authorization, Content-Type'
            }
        )
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
        }
        
        print("   CORS Headers:")
        for header, value in cors_headers.items():
            if value:
                print(f"      ✅ {header}: {value}")
            else:
                print(f"      ❌ {header}: Not set")
                
    except Exception as e:
        print(f"   ❌ CORS test failed: {e}")

if __name__ == "__main__":
    debug_network_connection()
    check_cors()
    
    print("\n" + "=" * 50)
    print("🎯 Troubleshooting Guide:")
    print("1. Make sure both servers are running:")
    print("   - API Server: python run.py (port 5000)")
    print("   - Dashboard: python admin_dashboard.py (port 8080)")
    print("2. Check browser console (F12) for specific error messages")
    print("3. Try uploading a small file first (under 1MB)")
    print("4. Check if firewall is blocking the connection")
    print("5. Make sure you're logged in with a valid token")
