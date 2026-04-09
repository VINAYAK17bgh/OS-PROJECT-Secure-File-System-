#!/usr/bin/env python3
"""
Example client for the Mini Secure File System API
Demonstrates how to interact with the secure file system programmatically.
"""

import requests
import json
import os

class SecureFileSystemClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.token = None
        self.user = None
    
    def register(self, username, email, password):
        """Register a new user"""
        data = {
            "username": username,
            "email": email,
            "password": password
        }
        
        response = requests.post(f"{self.base_url}/api/auth/register", json=data)
        
        if response.status_code == 201:
            print(f"✅ User {username} registered successfully")
            return True
        else:
            print(f"❌ Registration failed: {response.json().get('error', 'Unknown error')}")
            return False
    
    def login(self, username, password):
        """Login and get access token"""
        data = {
            "username": username,
            "password": password
        }
        
        response = requests.post(f"{self.base_url}/api/auth/login", json=data)
        
        if response.status_code == 200:
            result = response.json()
            self.token = result['access_token']
            self.user = result['user']
            print(f"✅ Login successful. Welcome {self.user['username']}!")
            return True
        else:
            print(f"❌ Login failed: {response.json().get('error', 'Unknown error')}")
            return False
    
    def get_profile(self):
        """Get user profile"""
        if not self.token:
            print("❌ Not logged in")
            return None
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.base_url}/api/auth/profile", headers=headers)
        
        if response.status_code == 200:
            return response.json()['user']
        else:
            print(f"❌ Failed to get profile: {response.json().get('error', 'Unknown error')}")
            return None
    
    def upload_file(self, file_path, is_public=False):
        """Upload a file"""
        if not self.token:
            print("❌ Not logged in")
            return None
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return None
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f, 'application/octet-stream')}
                data = {'is_public': str(is_public).lower()}
                headers = {"Authorization": f"Bearer {self.token}"}
                
                response = requests.post(
                    f"{self.base_url}/api/files/upload",
                    files=files,
                    data=data,
                    headers=headers
                )
            
            if response.status_code == 201:
                file_info = response.json()['file']
                print(f"✅ File uploaded successfully. File ID: {file_info['id']}")
                return file_info
            else:
                print(f"❌ Upload failed: {response.json().get('error', 'Unknown error')}")
                return None
        except Exception as e:
            print(f"❌ Upload error: {e}")
            return None
    
    def list_files(self):
        """List accessible files"""
        if not self.token:
            print("❌ Not logged in")
            return []
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.base_url}/api/files/list", headers=headers)
        
        if response.status_code == 200:
            files = response.json()['files']
            print(f"📁 Found {len(files)} files:")
            for file in files:
                status = "🌐 Public" if file['is_public'] else "🔒 Private"
                print(f"   - {file['original_filename']} ({status}) - {file['file_size']} bytes")
            return files
        else:
            print(f"❌ Failed to list files: {response.json().get('error', 'Unknown error')}")
            return []
    
    def download_file(self, file_id, save_path):
        """Download a file"""
        if not self.token:
            print("❌ Not logged in")
            return False
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.base_url}/api/files/{file_id}", headers=headers)
        
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ File downloaded to: {save_path}")
            return True
        else:
            print(f"❌ Download failed: {response.json().get('error', 'Unknown error')}")
            return False
    
    def delete_file(self, file_id):
        """Delete a file"""
        if not self.token:
            print("❌ Not logged in")
            return False
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.delete(f"{self.base_url}/api/files/{file_id}", headers=headers)
        
        if response.status_code == 200:
            print("✅ File deleted successfully")
            return True
        else:
            print(f"❌ Delete failed: {response.json().get('error', 'Unknown error')}")
            return False
    
    def logout(self):
        """Logout"""
        if not self.token:
            print("❌ Not logged in")
            return False
        
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(f"{self.base_url}/api/auth/logout", headers=headers)
        
        if response.status_code == 200:
            print("✅ Logged out successfully")
            self.token = None
            self.user = None
            return True
        else:
            print(f"❌ Logout failed: {response.json().get('error', 'Unknown error')}")
            return False

def demo():
    """Demonstrate the client functionality"""
    print("🔐 Secure File System Client Demo")
    print("=" * 40)
    
    client = SecureFileSystemClient()
    
    # Example 1: Register and login as a new user
    print("\n📝 1. Registering new user...")
    client.register("demo_user", "demo@example.com", "demo_password123")
    
    print("\n🔑 2. Logging in...")
    client.login("demo_user", "demo_password123")
    
    # Example 2: Create a test file and upload it
    print("\n📄 3. Creating test file...")
    test_file = "demo_test.txt"
    with open(test_file, 'w') as f:
        f.write("This is a test file for the Secure File System demo.\n")
        f.write("It will be encrypted and stored securely.\n")
    
    print("\n📤 4. Uploading file...")
    file_info = client.upload_file(test_file, is_public=False)
    
    if file_info:
        # Example 3: List files
        print("\n📋 5. Listing files...")
        files = client.list_files()
        
        # Example 4: Download the file
        print("\n📥 6. Downloading file...")
        downloaded_file = "downloaded_demo.txt"
        client.download_file(file_info['id'], downloaded_file)
        
        # Example 5: Delete the file
        print("\n🗑️ 7. Deleting file...")
        client.delete_file(file_info['id'])
    
    # Example 6: Logout
    print("\n👋 8. Logging out...")
    client.logout()
    
    # Cleanup
    for file in [test_file, "downloaded_demo.txt"]:
        if os.path.exists(file):
            os.remove(file)
    
    print("\n✅ Demo completed!")

def admin_demo():
    """Demonstrate admin functionality"""
    print("\n👑 Admin Demo")
    print("=" * 40)
    
    client = SecureFileSystemClient()
    
    # Login as admin
    print("\n🔑 Logging in as admin...")
    if client.login("admin", "admin123"):
        # Get admin stats (this would require admin routes)
        print("\n📊 Admin access granted!")
        print("   - You can now access admin endpoints")
        print("   - Visit http://localhost:8080 for the admin dashboard")
    
    client.logout()

if __name__ == "__main__":
    print("🚀 Starting Secure File System Client Demo")
    print("Make sure the server is running (python start.py)")
    print()
    
    try:
        demo()
        admin_demo()
        
        print("\n" + "=" * 40)
        print("🎉 All demos completed successfully!")
        print("\n💡 Next steps:")
        print("1. Open http://localhost:8080 in your browser")
        print("2. Login with admin/admin123")
        print("3. Explore the admin dashboard")
        print("4. Try uploading files through the web interface")
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("Make sure the server is running on http://localhost:5000")
