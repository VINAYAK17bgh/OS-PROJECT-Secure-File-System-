# Mini Secure File System

A comprehensive secure file management system with authentication, authorization, encryption, and monitoring capabilities.

## Features

### 🔐 Security Features
- **Secure Authentication**: JWT-based authentication with secure password hashing
- **Role-Based Access Control (RBAC)**: Admin, User, and Viewer roles with granular permissions
- **File-Level Encryption**: AES encryption for all stored files with unique per-file keys
- **Session Management**: Secure session tracking and management
- **Activity Logging**: Comprehensive audit trail of all system activities

### 👥 User Management
- Multi-user support with role-based permissions
- User registration, login, and profile management
- Admin dashboard for user management
- Account activation/deactivation

### 📁 File Management
- Secure file upload and download
- File encryption/decryption (transparent to users)
- File permission management (read, write, delete)
- Public and private file support
- File metadata tracking

### 📊 Monitoring & Analytics
- Real-time system statistics
- Activity log viewing and filtering
- Security monitoring and threat detection
- Suspicious activity alerts
- Admin dashboard with comprehensive metrics

### 🛡️ Security Features
- Failed login attempt tracking
- IP-based suspicious activity detection
- Unusual access pattern monitoring
- Secure key management
- Input validation and sanitization

## Architecture

```
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── routes/
│   │   ├── auth.py          # Authentication routes
│   │   ├── files.py         # File management routes
│   │   ├── admin.py         # Admin panel routes
│   │   └── logs.py          # Activity logging routes
│   └── utils/
│       ├── encryption.py    # File encryption utilities
│       └── decorators.py    # Security decorators
├── admin_dashboard/         # Web-based admin interface
│   ├── templates/
│   │   ├── index.html       # Main dashboard
│   │   └── login.html       # Login page
│   └── static/
│       └── js/
│           └── admin.js     # Dashboard JavaScript
├── uploads/                 # Encrypted file storage
├── config.py               # Configuration settings
├── run.py                  # Application entry point
├── admin_dashboard.py      # Admin dashboard server
└── requirements.txt        # Python dependencies
```

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup Steps

1. **Clone and navigate to the project**:
   ```bash
   cd path/to/project
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Unix
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Create required directories**:
   ```bash
   mkdir uploads
   ```

## Configuration

Edit the `.env` file with the following settings:

```env
SECRET_KEY=your-secret-key-here-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-here-change-in-production
DATABASE_URL=sqlite:///secure_file_system.db
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE=16777216
ENCRYPTION_KEY=your-encryption-key-32-chars-long
```

### Important Security Notes
- Change all secret keys in production
- Use a strong, randomly generated encryption key (32 characters)
- Consider using PostgreSQL for production databases
- Enable HTTPS in production

## Running the Application

### Method 1: Development Mode

1. **Start the main API server**:
   ```bash
   python run.py
   ```
   The API will be available at `http://localhost:5000`

2. **Start the admin dashboard** (in a new terminal):
   ```bash
   python admin_dashboard.py
   ```
   The dashboard will be available at `http://localhost:8080`

### Method 2: Production Mode

For production, use a WSGI server like Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## Default Credentials

After first run, a default admin account is created:
- **Username**: `admin`
- **Password**: `admin123`

⚠️ **Change this password immediately in production!**

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/logout` - User logout
- `GET /api/auth/profile` - Get user profile
- `POST /api/auth/change-password` - Change password

### File Management
- `POST /api/files/upload` - Upload file
- `GET /api/files/list` - List accessible files
- `GET /api/files/{id}` - Download file
- `GET /api/files/{id}/info` - Get file information
- `DELETE /api/files/{id}` - Delete file
- `POST /api/files/{id}/permissions` - Grant file permission
- `DELETE /api/files/{id}/permissions/{perm_id}` - Revoke permission

### Admin Panel
- `GET /api/admin/users` - List all users
- `GET /api/admin/users/{id}` - Get user details
- `PUT /api/admin/users/{id}/role` - Update user role
- `PUT /api/admin/users/{id}/status` - Update user status
- `DELETE /api/admin/users/{id}` - Delete user
- `GET /api/admin/files` - List all files
- `GET /api/admin/system/stats` - Get system statistics
- `GET /api/admin/security/suspicious-activity` - Get security alerts

### Activity Logs
- `GET /api/logs/` - Get activity logs
- `GET /api/logs/summary` - Get log summary
- `GET /api/logs/export` - Export logs
- `POST /api/logs/search` - Search logs

## Security Features

### Encryption
- All files are encrypted using AES-256
- Each file has a unique encryption key
- File keys are encrypted using a master key
- No plaintext files are stored on disk

### Authentication & Authorization
- JWT tokens with configurable expiration
- Role-based access control
- Session tracking and management
- Secure password hashing with bcrypt

### Monitoring & Logging
- Comprehensive activity logging
- Failed login attempt tracking
- Suspicious IP detection
- Unusual access pattern monitoring
- Real-time security alerts

## Usage Examples

### Register a New User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"password123"}'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"password123"}'
```

### Upload a File
```bash
curl -X POST http://localhost:5000/api/files/upload \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@/path/to/your/file.txt" \
  -F "is_public=false"
```

### List Files
```bash
curl -X GET http://localhost:5000/api/files/list \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Development

### Database Migrations
The application uses SQLAlchemy with automatic table creation. For production, consider using Alembic for database migrations.

### Testing
Run tests with:
```bash
python -m pytest tests/
```

### Adding New Features
1. Add models to `app/models.py`
2. Create routes in appropriate `app/routes/` file
3. Add security decorators as needed
4. Update admin dashboard if required

## Production Deployment

### Security Checklist
- [ ] Change all default passwords and keys
- [ ] Enable HTTPS
- [ ] Use environment variables for secrets
- [ ] Set up proper database backups
- [ ] Configure logging and monitoring
- [ ] Set up firewall rules
- [ ] Regular security updates

### Performance Considerations
- Use a production database (PostgreSQL recommended)
- Implement file storage with CDN for large deployments
- Consider Redis for session storage
- Set up proper caching strategies

## Troubleshooting

### Common Issues

1. **Database connection errors**: Check DATABASE_URL in .env
2. **Encryption errors**: Verify ENCRYPTION_KEY is 32 characters
3. **File upload failures**: Check upload directory permissions
4. **JWT token errors**: Verify JWT_SECRET_KEY is set

### Logs
Check application logs for detailed error information:
```bash
tail -f app.log
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Create an issue in the repository

---

**⚠️ Security Warning**: This is a demonstration project. Always conduct thorough security audits before deploying in production environments.
