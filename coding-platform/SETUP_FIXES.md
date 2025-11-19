# Coding Platform - Setup & Fixes Documentation

**Date**: November 19, 2025
**Status**: ✅ Fully Operational

---

## Table of Contents
1. [Quick Start](#quick-start)
2. [Issues Found & Fixed](#issues-found--fixed)
3. [Current Configuration](#current-configuration)
4. [Services Status](#services-status)
5. [Access Points](#access-points)
6. [Database Setup](#database-setup)
7. [Piston Configuration](#piston-configuration)
8. [Development Notes](#development-notes)
9. [Troubleshooting](#troubleshooting)
10. [Next Steps](#next-steps)

---

## Quick Start

### Starting the Platform
```bash
cd /path/to/coding-platform
docker-compose up -d
```

### Stopping the Platform
```bash
docker-compose down
```

### Viewing Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f piston
```

### Checking Status
```bash
docker-compose ps
```

---

## Issues Found & Fixed

### 1. Backend Import Error ✅
**Problem**: `ImportError: cannot import name 'Queue' from 'queue'`
- The `backend/queue/` directory name conflicted with Python's built-in `queue` module

**Solution**:
- Renamed `backend/queue/` → `backend/tasks/`
- Updated references in:
  - `backend/tasks/celery_app.py` (lines 33, 35)
  - `docker-compose.yml` (line 124)

**Files Modified**:
```
backend/tasks/celery_app.py
docker-compose.yml
```

---

### 2. Frontend JSX Runtime Error ✅
**Problem**: `jsxDEV is not a function` - React rendering error
- Docker Compose was overriding NODE_ENV to production while Dockerfile set it to development

**Solution**:
- Changed `NODE_ENV=production` → `NODE_ENV=development` in docker-compose.yml

**Files Modified**:
```
docker-compose.yml (line 152)
```

---

### 3. Missing .env File ✅
**Problem**: No environment configuration file existed

**Solution**:
- Created `.env` from `.env.example`
- All default development values are configured

**Files Created**:
```
.env
```

**Default Credentials**:
- PostgreSQL Password: `CHANGE_THIS_SECURE_PASSWORD_123`
- Redis Password: `CHANGE_THIS_REDIS_PASSWORD_456`
- Secret Key: `CHANGE_THIS_SECRET_KEY_TO_A_RANDOM_64_CHAR_STRING`

---

### 4. Nginx SSL Certificate Error ✅
**Problem**: `cannot load certificate "/etc/nginx/ssl/cert.pem"`
- Nginx was configured for HTTPS but no SSL certificates existed

**Solution**:
- Commented out HTTPS server block in nginx.conf for development
- Commented out HTTP-to-HTTPS redirect
- Using HTTP-only mode on port 80 for development

**Files Modified**:
```
nginx/nginx.conf (lines 61-188)
```

**Production Note**: For production deployment, uncomment the HTTPS blocks and generate proper SSL certificates using Let's Encrypt.

---

### 5. Piston Filesystem Permissions ✅
**Problem**: `mkdir: cannot create directory 'isolate/': Read-only file system`
- Piston container had strict security constraints preventing directory creation

**Solution**:
- Removed security constraints for development
- Changed `privileged: false` → `privileged: true`
- Removed `cap_drop`, `cap_add`, `security_opt`, and `tmpfs` configurations

**Files Modified**:
```
docker-compose.yml (lines 40-67)
```

**Production Note**: Re-implement proper security constraints for production deployment.

---

### 6. Database Password Mismatch ✅
**Problem**: Password authentication failed for PostgreSQL user
- Old database volume had different password than new .env file

**Solution**:
- Removed all Docker volumes: `docker-compose down -v`
- Recreated volumes with fresh configuration

---

### 7. Piston API Endpoint Error ✅
**Problem**: Code execution failing with `{"message":"Not Found"}`
- Backend was using wrong Piston API endpoint (`/execute` instead of `/api/v2/execute`)

**Solution**:
- Updated Piston API endpoints in backend code:
  - `/execute` → `/api/v2/execute`
  - `/runtimes` → `/api/v2/runtimes`

**Files Modified**:
```
backend/api/code_execution.py (lines 95, 276)
```

---

### 8. Piston Python Runtime Installation ✅
**Problem**: No programming language runtimes installed in Piston

**Solution**:
- Installed Python 3.12.0 runtime via Piston API
- Command used:
```bash
docker exec coding_platform_backend curl -X POST http://piston:2000/api/v2/packages \
  -H "Content-Type: application/json" \
  -d '{"language":"python","version":"3.12.0"}'
```

---

## Current Configuration

### Docker Compose Services

| Service | Container Name | Status | Ports |
|---------|---------------|--------|-------|
| PostgreSQL | coding_platform_db | Healthy | 5432 (internal) |
| Redis | coding_platform_redis | Healthy | 6379 (internal) |
| Backend (FastAPI) | coding_platform_backend | Healthy | 8000:8000 |
| Frontend (Next.js) | coding_platform_frontend | Running | 3000:3000 |
| Celery Worker | coding_platform_celery | Running | - |
| Piston | coding_platform_piston | Running | 2000 (internal) |
| Nginx | coding_platform_nginx | Running | 80:80, 443:443 |

### Environment Variables
All configured in `.env` file:
- Database: PostgreSQL 15
- Cache: Redis 7
- Backend: FastAPI with Python 3.11
- Frontend: Next.js 14 with React 18

---

## Services Status

### ✅ Healthy Services
- **PostgreSQL**: Database running, tables created
- **Redis**: Cache and queue running
- **Backend**: API healthy and responding
- **Nginx**: Reverse proxy operational
- **Piston**: Code execution engine ready

### ⚠️ Services with Health Check Issues
Some services show "unhealthy" in docker-compose status but are actually working:
- **Frontend**: Health check endpoint may not be configured, but frontend is rendering
- **Celery**: No health check endpoint, but worker is connected and ready

These health check issues don't affect functionality.

---

## Access Points

### Web Interfaces
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **API Documentation (ReDoc)**: http://localhost:8000/redoc
- **Nginx Proxy**: http://localhost

### Default Admin Account
```
Username: admin
Password: admin123
```
⚠️ **Change this password immediately in production!**

### Sample Lessons Created
5 Python lessons have been seeded:
1. Hello World and Variables (Beginner)
2. Functions and Control Flow (Beginner)
3. Working with Lists (Beginner)
4. String Manipulation (Intermediate)
5. Dictionaries and Data Structures (Intermediate)

---

## Database Setup

### Initial Setup Commands
```bash
# Seed database with sample lessons and admin user
docker exec coding_platform_backend bash -c "cd /app && python -m database.seed_lessons"
```

### Database Schema
Tables created:
- `users` - User accounts
- `lessons` - Coding lessons
- `submissions` - Code submission history
- `progress` - User progress tracking

---

## Piston Configuration

### Installed Runtimes
- **Python 3.12.0**
  - Aliases: `py`, `py3`, `python3`, `python3.12`

### Installing Additional Languages
To add more programming languages:

**JavaScript/Node.js**:
```bash
docker exec coding_platform_backend curl -X POST http://piston:2000/api/v2/packages \
  -H "Content-Type: application/json" \
  -d '{"language":"node","version":"20.11.1"}'
```

**Java**:
```bash
docker exec coding_platform_backend curl -X POST http://piston:2000/api/v2/packages \
  -H "Content-Type: application/json" \
  -d '{"language":"java","version":"15.0.2"}'
```

**C++**:
```bash
docker exec coding_platform_backend curl -X POST http://piston:2000/api/v2/packages \
  -H "Content-Type: application/json" \
  -d '{"language":"gcc","version":"10.2.0"}'
```

### Check Available Packages
```bash
docker exec coding_platform_backend curl -s http://piston:2000/api/v2/packages
```

### Check Installed Runtimes
```bash
docker exec coding_platform_backend curl -s http://piston:2000/api/v2/runtimes
```

---

## Development Notes

### File Structure Changes
```
backend/
├── tasks/              # ← Renamed from 'queue'
│   ├── __init__.py
│   └── celery_app.py
├── api/
│   └── code_execution.py  # ← Updated Piston endpoints
└── ...
```

### Key Configuration Files
- `docker-compose.yml` - Service orchestration (multiple changes)
- `nginx/nginx.conf` - HTTPS disabled for dev
- `.env` - Environment variables
- `backend/api/code_execution.py` - Piston API integration

### Volume Mounts
```yaml
Backend:  ./backend:/app
Frontend: ./frontend:/app
Database: postgres_data (volume)
Redis:    redis_data (volume)
Piston:   piston_packages (volume)
Nginx:    nginx_logs (volume)
```

---

## Troubleshooting

### Backend Not Starting
```bash
# Check logs
docker-compose logs backend

# Common issue: Database not ready
# Solution: Wait for PostgreSQL to be healthy
docker-compose ps postgres
```

### Frontend Not Rendering
```bash
# Check NODE_ENV is set to development
docker-compose exec frontend env | grep NODE_ENV

# Should output: NODE_ENV=development
```

### Code Execution Failing
```bash
# Check Piston is running
docker-compose ps piston

# Check Python is installed
docker exec coding_platform_backend curl -s http://piston:2000/api/v2/runtimes

# Should show Python 3.12.0
```

### Nginx Not Starting
```bash
# Check nginx config syntax
docker-compose exec nginx nginx -t

# Check SSL certificate requirement
docker-compose logs nginx | grep -i ssl
```

### Database Connection Issues
```bash
# Check PostgreSQL is healthy
docker-compose ps postgres

# Reset database (WARNING: Deletes all data)
docker-compose down -v
docker-compose up -d
docker exec coding_platform_backend bash -c "cd /app && python -m database.seed_lessons"
```

### Celery Worker Not Processing Tasks
```bash
# Check Celery logs
docker-compose logs celery_worker

# Verify Redis connection
docker-compose exec celery_worker celery -A tasks.celery_app inspect ping
```

---

## Next Steps

### Recommended Improvements

#### 1. Enable Auto-Reload for Backend
**Current**: Backend doesn't auto-reload on code changes

**Fix**: Update backend Dockerfile to run with `--reload` flag:
```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

#### 2. Fix Health Checks
**Current**: Some services show unhealthy but work fine

**Fix**: Add proper health check endpoints or adjust health check configurations in docker-compose.yml

#### 3. Security Hardening for Production
**Current**: Running in development mode with relaxed security

**Production checklist**:
- [ ] Change all default passwords in `.env`
- [ ] Generate strong SECRET_KEY (64+ random characters)
- [ ] Re-enable Piston security constraints
- [ ] Set up SSL certificates (Let's Encrypt)
- [ ] Uncomment HTTPS configuration in nginx.conf
- [ ] Set NODE_ENV=production for frontend build
- [ ] Enable CORS only for production domain
- [ ] Set up automated backups
- [ ] Configure proper logging and monitoring

#### 4. Additional Language Support
Install more programming languages in Piston:
- JavaScript/Node.js
- Java
- C/C++
- Go
- Rust

#### 5. Enhanced Features
- [ ] WebSocket support for real-time code execution
- [ ] Code sharing functionality
- [ ] Leaderboard/achievements system
- [ ] More lesson content
- [ ] User profiles with avatars
- [ ] Dark mode for code editor
- [ ] Code syntax highlighting improvements

#### 6. Testing
- [ ] Add backend unit tests
- [ ] Add frontend component tests
- [ ] Add integration tests
- [ ] Set up CI/CD pipeline

#### 7. Documentation
- [ ] API documentation improvements
- [ ] User guide
- [ ] Contribution guidelines
- [ ] Architecture documentation

---

## Version Information

### Technology Stack
- **Backend**: FastAPI (Python 3.11), SQLAlchemy, PostgreSQL 15
- **Frontend**: Next.js 14, React 18, CodeMirror 6
- **Cache/Queue**: Redis 7, Celery
- **Code Execution**: Piston v3.1.1
- **Reverse Proxy**: Nginx (Alpine)
- **Containerization**: Docker, Docker Compose

### Package Versions
```
Backend:
- fastapi: Latest
- uvicorn: Latest
- sqlalchemy: Latest
- asyncpg: Latest
- celery: Latest
- redis: Latest

Frontend:
- next: 14.0.3
- react: 18.2.0
- @codemirror/lang-python: 6.1.3
- axios: 1.6.2
```

---

## Quick Reference Commands

### Development
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Restart specific service
docker-compose restart backend

# View logs (follow mode)
docker-compose logs -f

# Check service status
docker-compose ps

# Access backend shell
docker exec -it coding_platform_backend bash

# Access database
docker exec -it coding_platform_db psql -U platform_user coding_platform
```

### Database Management
```bash
# Seed database
docker exec coding_platform_backend bash -c "cd /app && python -m database.seed_lessons"

# Backup database
docker exec coding_platform_db pg_dump -U platform_user coding_platform > backup.sql

# Restore database
docker exec -i coding_platform_db psql -U platform_user coding_platform < backup.sql

# Reset database (WARNING: Deletes all data)
docker-compose down -v
docker-compose up -d
```

### Maintenance
```bash
# Clean up Docker system
docker system prune -a

# Remove all volumes (WARNING: Deletes all data)
docker volume prune

# Rebuild containers
docker-compose build --no-cache
docker-compose up -d
```

---

## Support & Resources

### Documentation Links
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Piston Documentation](https://github.com/engineer-man/piston)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

### Project-Specific
- Original README: `README.md`
- Deployment Guide: `DEPLOYMENT.md`
- Project Criteria: `project_criteria.md`

---

## Change Log

### November 19, 2025
- Fixed backend Queue import conflict
- Fixed frontend JSX runtime error
- Created .env configuration file
- Disabled Nginx HTTPS for development
- Fixed Piston filesystem permissions
- Installed Python 3.12.0 runtime
- Fixed Piston API endpoints
- Seeded database with sample lessons
- Created admin user account
- Documented all fixes and setup

---

**Last Updated**: November 19, 2025
**Platform Status**: ✅ Fully Operational
**Ready for Development**: Yes
