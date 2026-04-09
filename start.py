#!/usr/bin/env python3
"""
Startup script for the Mini Secure File System
This script initializes the system and starts both servers.
"""

import subprocess
import sys
import os
import time
import signal
import webbrowser
from threading import Thread

def check_dependencies():
    """Check if all required packages are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = {
        'flask': 'flask',
        'flask_sqlalchemy': 'flask_sqlalchemy', 
        'flask_jwt_extended': 'flask_jwt_extended',
        'flask_cors': 'flask_cors',
        'bcrypt': 'bcrypt',
        'cryptography': 'cryptography',
        'python_dotenv': 'dotenv',
        'marshmallow': 'marshmallow',
        'werkzeug': 'werkzeug'
    }
    
    missing_packages = []
    
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install them with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def setup_environment():
    """Set up environment variables and directories"""
    print("🔧 Setting up environment...")
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        print("Creating .env file...")
        with open('.env.example', 'r') as f:
            env_content = f.read()
        
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created from template")
    
    # Create uploads directory
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
        print("✅ Uploads directory created")
    
    # Create database and admin user
    print("🗄️ Initializing database...")
    try:
        from app import create_app, db
        from app.models import User, UserRole
        from cryptography.fernet import Fernet
        
        # Generate encryption key if not exists
        if not os.path.exists('.env'):
            print("Creating .env file...")
            with open('.env.example', 'r') as f:
                env_content = f.read()
            
            # Generate a proper encryption key
            encryption_key = Fernet.generate_key().decode()
            env_content = env_content.replace('your-encryption-key-32-chars-long', encryption_key)
            
            with open('.env', 'w') as f:
                f.write(env_content)
            print("✅ .env file created with encryption key")
        
        app = create_app()
        with app.app_context():
            db.create_all()
            
            admin_user = User.query.filter_by(username='admin').first()
            if not admin_user:
                admin_user = User(
                    username='admin',
                    email='admin@example.com',
                    role=UserRole.ADMIN
                )
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                db.session.commit()
                print("✅ Default admin user created")
            else:
                print("✅ Admin user already exists")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False
    
    return True

def start_api_server():
    """Start the main API server"""
    print("🚀 Starting API server on port 5000...")
    try:
        process = subprocess.Popen([sys.executable, 'run.py'])
        return process
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        return None

def start_dashboard():
    """Start the admin dashboard"""
    print("🖥️ Starting admin dashboard on port 8080...")
    try:
        process = subprocess.Popen([sys.executable, 'admin_dashboard.py'])
        return process
    except Exception as e:
        print(f"❌ Failed to start admin dashboard: {e}")
        return None

def wait_for_server(url, timeout=30):
    """Wait for a server to be ready"""
    import requests
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=1)
            if response.status_code in [200, 401]:  # 401 is OK for API (means it's running)
                return True
        except:
            pass
        time.sleep(1)
    return False

def open_browser():
    """Open browser to the admin dashboard"""
    print("🌐 Opening browser...")
    time.sleep(3)  # Wait for servers to start
    try:
        webbrowser.open('http://localhost:8080')
        print("✅ Browser opened to admin dashboard")
    except Exception as e:
        print(f"⚠️ Could not open browser automatically: {e}")
        print("Please manually open http://localhost:8080 in your browser")

def main():
    """Main startup function"""
    print("🔐 Mini Secure File System Startup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Start servers
    api_process = start_api_server()
    dashboard_process = start_dashboard()
    
    if not api_process or not dashboard_process:
        print("❌ Failed to start servers")
        if api_process:
            api_process.terminate()
        if dashboard_process:
            dashboard_process.terminate()
        sys.exit(1)
    
    # Wait for servers to be ready
    print("⏳ Waiting for servers to start...")
    
    # Start browser opening in background
    browser_thread = Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    api_ready = wait_for_server('http://localhost:5000/api/auth/profile')
    dashboard_ready = wait_for_server('http://localhost:8080')
    
    if api_ready and dashboard_ready:
        print("\n✅ System started successfully!")
        print("\n📋 Access Information:")
        print("   🖥️  Admin Dashboard: http://localhost:8080")
        print("   🔌 API Server: http://localhost:5000")
        print("   👤 Default Admin: admin / admin123")
        print("\n🛑 Press Ctrl+C to stop all servers")
        
        try:
            # Keep the script running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down servers...")
            if api_process:
                api_process.terminate()
            if dashboard_process:
                dashboard_process.terminate()
            print("✅ All servers stopped")
    else:
        print("❌ Servers failed to start properly")
        if api_process:
            api_process.terminate()
        if dashboard_process:
            dashboard_process.terminate()
        sys.exit(1)

if __name__ == "__main__":
    main()
