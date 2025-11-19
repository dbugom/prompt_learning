# Coding Education Platform

A complete, production-ready interactive coding education platform with secure code execution, real-time feedback, and progress tracking. **Now with enhanced accessibility, professional UX improvements, and advanced user experience features.**

## ✨ Features

### Core Features
- **Interactive Code Editor**: CodeMirror 6 with syntax highlighting for multiple languages
- **Secure Code Execution**: Sandboxed execution via Piston engine with resource limits
- **Real-Time Feedback**: Instant code execution results and test case validation
- **Progress Tracking**: Track user progress through lessons with detailed analytics
- **User Authentication**: JWT-based authentication with secure password hashing
- **Responsive Design**: Mobile-friendly UI that works on all devices
- **RESTful API**: Comprehensive API with OpenAPI/Swagger documentation
- **Production Ready**: Docker-based deployment with security hardening

### 🆕 Enhanced UX Features (2024)

#### Accessibility & Inclusivity
- **WCAG 2.1 AA Compliant**: Improved color contrast for better readability
- **Full Keyboard Navigation**: Complete keyboard support with intuitive shortcuts
- **Screen Reader Compatible**: Proper ARIA labels and semantic HTML throughout
- **Focus Management**: Advanced focus trapping in modals and dialogs
- **Reduced Motion Support**: Respects user's motion preferences
- **High Contrast Mode**: Enhanced visibility for users with visual impairments
- **Skip Navigation Links**: Quick access to main content for keyboard users

#### User Experience Enhancements
- **Auto-Save Functionality**: Never lose your work - code is automatically saved to local storage
- **Visual Save Status**: Real-time feedback showing save status (Saving/Saved/Error)
- **Smart Error Messages**: Contextual, helpful error messages with retry mechanisms
- **Loading Skeletons**: Professional loading states that match content structure
- **Session Management**: Automatic session timeout warnings with extension option
- **Accessible Modals**: Custom modal dialogs with proper focus management
- **Password Strength Indicator**: Real-time password strength visualization
- **Show/Hide Password**: Toggle password visibility for easier input
- **Real-Time Form Validation**: Instant feedback on form fields with helpful error messages
- **Code Formatting**: One-click code formatting to clean up spacing and indentation

#### Keyboard Shortcuts
- **⌘/Ctrl + Enter**: Run code and execute tests
- **⌘/Ctrl + R**: Reset code to starter template
- **Shift + Alt + F**: Format code automatically
- **Esc**: Clear output console
- **⌘/Ctrl + /**: Display keyboard shortcuts help
- **Tab/Shift+Tab**: Navigate between interactive elements

#### Developer Experience
- **Code Auto-Formatting**: Clean up code with a single click
- **Retry Failed Operations**: Automatic retry for network errors (up to 3 attempts)
- **Persistent Code State**: Code restoration on page refresh
- **Visual Keyboard Hints**: On-screen display of available shortcuts
- **Smart Validation**: Field-level validation with helpful guidance

## Tech Stack

### Frontend
- **Next.js 14**: React framework with SSR/SSG
- **CodeMirror 6**: Advanced code editor with Python syntax highlighting
- **Axios**: HTTP client for API communication with centralized error handling
- **React Hot Toast**: Beautiful, accessible notifications

### Backend
- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Relational database for user data and progress
- **Redis**: Caching and session management
- **Celery**: Asynchronous task queue
- **SQLAlchemy**: ORM for database operations
- **Piston**: Secure code execution engine (Python 3.10.0)

### Infrastructure
- **Docker & Docker Compose**: Containerization and orchestration
- **Nginx**: Reverse proxy with SSL/TLS termination
- **Ubuntu 22.04 LTS**: Server operating system
- **Let's Encrypt**: Free SSL certificates

### Accessibility
- **WCAG 2.1 AA Compliant**: Color contrast ratios meet accessibility standards
- **ARIA**: Comprehensive ARIA labels and semantic HTML
- **Keyboard Navigation**: Full keyboard support with skip links
- **LocalStorage**: Client-side code persistence and auto-save

## System Requirements

### Development
- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum
- 10GB disk space

### Production (Hetzner CX32 or similar)
- 4 vCPUs
- 8GB RAM
- 80GB SSD
- Ubuntu 22.04 LTS
- Public IP address

## Quick Start (Development)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd coding-platform
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Start Services

```bash
docker-compose up -d
```

### 4. Seed Sample Lessons

```bash
docker exec -it coding_platform_backend python database/seed_lessons.py
```

### 5. Access the Platform

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc

### Default Admin Credentials (After Seeding)

- **Username**: admin
- **Password**: admin123
- **⚠️ Change immediately in production!**

## Project Structure

```
coding-platform/
├── docker-compose.yml           # Docker services configuration
├── .env                        # Environment variables
├── frontend/                   # Next.js frontend application
│   ├── pages/                 # Next.js pages
│   ├── components/            # React components
│   ├── styles/               # CSS modules
│   └── utils/                # Utility functions
├── backend/                   # FastAPI backend application
│   ├── main.py               # FastAPI entry point
│   ├── api/                  # API endpoints
│   ├── models/               # Database models
│   ├── database/             # Database configuration
│   ├── queue/                # Celery tasks
│   └── tests/                # API tests
├── nginx/                    # Nginx configuration
│   └── nginx.conf           # Reverse proxy config
└── deployment/              # Deployment scripts
    ├── setup.sh            # System setup script
    ├── security-hardening.sh  # Security configuration
    └── hetzner-deploy.sh      # Automated deployment
```

## API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login and get JWT token |
| GET | `/api/auth/me` | Get current user info |
| GET | `/api/auth/verify` | Verify token validity |

### Lessons Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/lessons` | Get all lessons |
| GET | `/api/lessons/{id}` | Get lesson by ID |
| GET | `/api/lessons/slug/{slug}` | Get lesson by slug |
| POST | `/api/lessons` | Create lesson (admin) |
| PUT | `/api/lessons/{id}` | Update lesson (admin) |
| DELETE | `/api/lessons/{id}` | Delete lesson (admin) |

### Code Execution Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/code/execute` | Execute code |
| GET | `/api/code/runtimes` | Get available runtimes |
| GET | `/api/code/submissions` | Get user submissions |
| GET | `/api/code/submissions/{id}` | Get submission by ID |

### Progress Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/progress/overview` | Get progress overview |
| GET | `/api/progress/lessons` | Get lessons with progress |
| GET | `/api/progress/lesson/{id}` | Get lesson progress |
| POST | `/api/progress/lesson/{id}` | Update lesson progress |
| DELETE | `/api/progress/lesson/{id}` | Reset lesson progress |

## Testing

### Backend Tests

```bash
# Run all tests
docker exec -it coding_platform_backend pytest

# Run with coverage
docker exec -it coding_platform_backend pytest --cov

# Run specific test file
docker exec -it coding_platform_backend pytest tests/test_api.py
```

### Load Testing

```bash
# Install locust
pip install locust

# Run load tests
locust -f backend/tests/load_test.py --host=http://localhost:8000

# Open browser to http://localhost:8089 for UI
```

## Security Features

- **Authentication**: JWT tokens with secure password hashing (bcrypt)
- **Code Execution**: Sandboxed containers with resource limits
- **Rate Limiting**: API rate limiting (10 req/min by default)
- **CORS**: Configured Cross-Origin Resource Sharing
- **Security Headers**: X-Frame-Options, CSP, HSTS
- **Input Validation**: Pydantic models for request validation
- **SQL Injection Prevention**: ORM with parameterized queries
- **XSS Protection**: Content sanitization

## Monitoring

### Health Checks

```bash
# Check all services
docker-compose ps

# Check API health
curl http://localhost:8000/health

# Check frontend health
curl http://localhost:3000
```

### Logs

```bash
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# View recent logs
docker-compose logs --tail=100 backend
```

### Resource Usage

```bash
# Monitor container resources
docker stats

# Monitor from within server
htop
iotop
```

## Backup

### Manual Backup

```bash
# Backup database
docker exec coding_platform_db pg_dump -U platform_user coding_platform > backup.sql

# Backup environment
cp .env .env.backup

# Restore database
docker exec -i coding_platform_db psql -U platform_user coding_platform < backup.sql
```

### Automated Backups

Backups are automatically created daily at 2 AM when deployed via deployment scripts.

```bash
# Check backups
ls -lh /var/backups/coding-platform/

# Restore from backup
tar -xzf /var/backups/coding-platform/backup_YYYYMMDD.tar.gz
```

## Troubleshooting

### Services Won't Start

```bash
# Check Docker is running
sudo systemctl status docker

# Check logs for errors
docker-compose logs

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check connection
docker exec coding_platform_backend python -c "from database.connection import init_db; import asyncio; asyncio.run(init_db())"
```

### Code Execution Fails

```bash
# Check Piston is running
docker-compose ps piston

# Check Piston health
curl http://localhost:2000/runtimes

# Restart Piston
docker-compose restart piston
```

### Port Already in Use

```bash
# Find process using port
sudo lsof -i :8000
sudo lsof -i :3000

# Kill process
sudo kill -9 <PID>

# Or change port in docker-compose.yml
```

## Performance Optimization

### Database

- Indexes are automatically created on frequently queried fields
- Connection pooling via SQLAlchemy
- Query optimization with async operations

### Frontend

- Next.js automatic code splitting
- Static asset caching
- Image optimization

### Backend

- Async/await for non-blocking operations
- Redis caching for frequently accessed data
- Rate limiting to prevent abuse

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Contact: admin@example.com

## Acknowledgments

- [Piston](https://github.com/engineer-man/piston) - Code execution engine
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Next.js](https://nextjs.org/) - React framework
- [CodeMirror](https://codemirror.net/) - Code editor component
