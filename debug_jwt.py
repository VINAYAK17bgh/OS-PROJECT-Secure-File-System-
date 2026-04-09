#!/usr/bin/env python3
import requests
import json
import base64

def debug_jwt():
    """Debug JWT token issues"""
    
    print("🔍 Debugging JWT Token Issues")
    print("=" * 40)
    
    # Step 1: Login and get token
    print("\n1. Getting JWT token...")
    login_data = {"username": "admin", "password": "admin123"}
    
    try:
        response = requests.post("http://localhost:5000/api/auth/login", json=login_data)
        
        if response.status_code == 200:
            token = response.json()['access_token']
            print(f"✅ Token received: {token[:50]}...")
            
            # Step 2: Decode token to check its structure
            print("\n2. Decoding JWT token...")
            try:
                # JWT tokens have 3 parts separated by dots
                parts = token.split('.')
                print(f"Token parts: {len(parts)}")
                
                if len(parts) == 3:
                    # Decode header
                    header = base64.urlsafe_b64decode(parts[0] + '==').decode()
                    print(f"Header: {header}")
                    
                    # Decode payload
                    payload = base64.urlsafe_b64decode(parts[1] + '==').decode()
                    print(f"Payload: {payload}")
                else:
                    print("❌ Invalid JWT format")
                    
            except Exception as e:
                print(f"❌ Token decode error: {e}")
            
            # Step 3: Test API call with different header formats
            print("\n3. Testing API calls...")
            
            headers_variations = [
                {"Authorization": f"Bearer {token}"},
                {"Authorization": token},
                {"X-Access-Token": token},
                {"token": token}
            ]
            
            for i, headers in enumerate(headers_variations):
                print(f"\n   Test {i+1}: {headers}")
                try:
                    response = requests.get("http://localhost:5000/api/auth/profile", headers=headers)
                    print(f"   Status: {response.status_code}")
                    if response.status_code == 200:
                        print("   ✅ Success!")
                        break
                    else:
                        print(f"   Response: {response.text}")
                except Exception as e:
                    print(f"   Error: {e}")
            
            # Step 4: Test without any auth
            print("\n4. Testing without authentication...")
            try:
                response = requests.get("http://localhost:5000/api/auth/profile")
                print(f"Status: {response.status_code}")
                print(f"Response: {response.text}")
            except Exception as e:
                print(f"Error: {e}")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Login error: {e}")

if __name__ == "__main__":
    debug_jwt()
