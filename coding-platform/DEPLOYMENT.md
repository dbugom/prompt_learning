# Deployment Guide for Hetzner Cloud

Complete step-by-step guide to deploy the Coding Education Platform on Hetzner Cloud.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Server Provisioning](#server-provisioning)
3. [Initial Server Setup](#initial-server-setup)
4. [Automated Deployment](#automated-deployment)
5. [Manual Deployment](#manual-deployment)
6. [SSL Configuration](#ssl-configuration)
7. [DNS Configuration](#dns-configuration)
8. [Post-Deployment](#post-deployment)
9. [Maintenance](#maintenance)
10. [Troubleshooting](#troubleshooting)

## Prerequisites

### Local Machine
- SSH key pair generated
- Git installed
- Domain name (optional but recommended)

### Hetzner Account
- Hetzner Cloud account
- Payment method added
- API token (if using automated provisioning)

### Recommended Server
- **Type**: CX32 or better
- **vCPUs**: 4
- **RAM**: 8 GB
- **Storage**: 80 GB SSD
- **OS**: Ubuntu 22.04 LTS
- **Location**: Choose nearest to your users

## Server Provisioning

### Option 1: Hetzner Cloud Console (Recommended for Beginners)

1. **Login to Hetzner Cloud**
   - Go to https://console.hetzner.cloud/
   - Login with your credentials

2. **Create New Project**
   - Click "New Project"
   - Name: "coding-platform-prod"

3. **Create Server**
   - Click "Add Server"
   - **Location**: Choose your preferred location (e.g., Nuremberg)
   - **Image**: Ubuntu 22.04
   - **Type**: CX32 (4 vCPUs, 8 GB RAM, 80 GB SSD)
   - **Networking**:
     - IPv4 ✓
     - IPv6 ✓ (optional)
   - **SSH Keys**: Add your public SSH key
   - **Name**: coding-platform-server
   - Click "Create & Buy Now"

4. **Note Server IP**
   - Copy the IPv4 address (e.g., 65.108.x.x)

### Option 2: Hetzner CLI (For Advanced Users)

```bash
# Install hcloud CLI
brew install hcloud  # macOS
# or
snap install hcloud  # Linux

# Login
hcloud context create coding-platform

# Create server
hcloud server create \
  --name coding-platform-server \
  --type cx32 \
  --image ubuntu-22.04 \
  --ssh-key <your-key-id> \
  --location nbg1

# Get server IP
hcloud server ip coding-platform-server
```

## Initial Server Setup

### 1. Connect to Server

```bash
ssh root@YOUR_SERVER_IP
```

### 2. Update System

```bash
apt-get update && apt-get upgrade -y
```

### 3. Create Non-Root User (Recommended)

```bash
# Create user
adduser deployer

# Add to sudo group
usermod -aG sudo deployer

# Copy SSH keys
mkdir -p /home/deployer/.ssh
cp /root/.ssh/authorized_keys /home/deployer/.ssh/
chown -R deployer:deployer /home/deployer/.ssh
chmod 700 /home/deployer/.ssh
chmod 600 /home/deployer/.ssh/authorized_keys

# Test connection (from local machine)
ssh deployer@YOUR_SERVER_IP
```

### 4. Configure Firewall (Hetzner Cloud Firewall)

In Hetzner Cloud Console:
- Go to Firewalls
- Create new firewall "web-server"
- **Inbound Rules**:
  - SSH (22) - Your IP or 0.0.0.0/0
  - HTTP (80) - 0.0.0.0/0
  - HTTPS (443) - 0.0.0.0/0
- **Outbound Rules**: Allow all
- Attach to your server

## Automated Deployment

### Method 1: One-Command Deployment

```bash
# On your local machine, upload files
scp -r coding-platform root@YOUR_SERVER_IP:/tmp/

# SSH into server
ssh root@YOUR_SERVER_IP

# Run automated deployment
cd /tmp/coding-platform/deployment
chmod +x *.sh
./hetzner-deploy.sh
```

This script will:
- ✓ Install Docker and Docker Compose
- ✓ Configure firewall (UFW)
- ✓ Apply security hardening
- ✓ Copy application files
- ✓ Generate secure passwords
- ✓ Start all services
- ✓ Set up automated backups

**Estimated time**: 10-15 minutes

### Method 2: Step-by-Step Automated

```bash
# 1. Run system setup
./deployment/setup.sh

# 2. Run security hardening
./deployment/security-hardening.sh

# 3. Deploy application
cd /opt/coding-platform
docker-compose up -d

# 4. Seed sample lessons
docker exec -it coding_platform_backend python database/seed_lessons.py
```

## Manual Deployment

If you prefer manual control:

### 1. Install Docker

```bash
# Install prerequisites
apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

# Add Docker GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io

# Start Docker
systemctl start docker
systemctl enable docker
```

### 2. Install Docker Compose

```bash
# Download Docker Compose
curl -SL "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make executable
chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version
```

### 3. Clone Repository

```bash
# Install Git
apt-get install -y git

# Clone repository
cd /opt
git clone <your-repository-url> coding-platform
cd coding-platform
```

### 4. Configure Environment

```bash
# Copy example env
cp .env.example .env

# Generate secure passwords
POSTGRES_PASSWORD=$(openssl rand -base64 32)
REDIS_PASSWORD=$(openssl rand -base64 32)
SECRET_KEY=$(openssl rand -base64 64)

# Update .env file
nano .env
```

Update these values:
```env
POSTGRES_PASSWORD=<generated-password>
REDIS_PASSWORD=<generated-password>
SECRET_KEY=<generated-secret>
NEXT_PUBLIC_API_URL=https://yourdomain.com/api
NEXT_PUBLIC_WS_URL=wss://yourdomain.com/ws
ALLOWED_ORIGINS=https://yourdomain.com
DOMAIN=yourdomain.com
ADMIN_EMAIL=admin@yourdomain.com
```

### 5. Start Services

```bash
# Pull images
docker-compose pull

# Build custom images
docker-compose build

# Start services
docker-compose up -d

# Check status
docker-compose ps
```

### 6. Initialize Database

```bash
# Seed sample lessons
docker exec -it coding_platform_backend python database/seed_lessons.py
```

## SSL Configuration

### Option 1: Let's Encrypt (Recommended for Production)

```bash
# Install Certbot
apt-get install -y certbot python3-certbot-nginx

# Stop Nginx temporarily
docker-compose stop nginx

# Obtain certificate
certbot certonly --standalone \
  -d yourdomain.com \
  -d www.yourdomain.com \
  --email admin@yourdomain.com \
  --agree-tos \
  --non-interactive

# Copy certificates
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem /opt/coding-platform/nginx/ssl/cert.pem
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem /opt/coding-platform/nginx/ssl/key.pem

# Start Nginx
docker-compose start nginx

# Set up auto-renewal
echo "0 3 * * * certbot renew --quiet --deploy-hook 'docker-compose -f /opt/coding-platform/docker-compose.yml restart nginx'" | crontab -
```

### Option 2: Self-Signed Certificate (Development Only)

```bash
# Generate certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /opt/coding-platform/nginx/ssl/key.pem \
  -out /opt/coding-platform/nginx/ssl/cert.pem \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=yourdomain.com"

# Restart Nginx
docker-compose restart nginx
```

## DNS Configuration

### Configure DNS Records

Point your domain to your server IP:

```
# A Records
yourdomain.com.       A    YOUR_SERVER_IP
www.yourdomain.com.   A    YOUR_SERVER_IP

# AAAA Records (if using IPv6)
yourdomain.com.       AAAA YOUR_SERVER_IPv6
www.yourdomain.com.   AAAA YOUR_SERVER_IPv6
```

**DNS Providers:**
- Cloudflare (recommended): Free, fast DNS
- AWS Route 53: Advanced features
- Hetzner DNS: Integrated with Hetzner

**Propagation Time**: 1-48 hours (usually 1-2 hours)

## Post-Deployment

### 1. Create Admin User

```bash
# Option 1: Use the seeded admin user
# Username: admin
# Password: admin123
# ⚠️ Change password immediately!

# Option 2: Register through UI
# Visit https://yourdomain.com/register
```

### 2. Verify Services

```bash
# Check all containers are running
docker-compose ps

# Check logs
docker-compose logs -f

# Test endpoints
curl https://yourdomain.com/health
curl https://yourdomain.com/api/lessons
```

### 3. Create Sample Lessons

```bash
# Already done if you ran seed_lessons.py
# Or create through admin interface
```

### 4. Configure Backups

Backups are automatically configured if you used deployment scripts.

Manual setup:
```bash
# Create backup script
cat > /usr/local/bin/backup-platform <<'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/coding-platform"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup database
docker exec coding_platform_db pg_dump -U platform_user coding_platform > $BACKUP_DIR/db_$DATE.sql

# Backup environment
cp /opt/coding-platform/.env $BACKUP_DIR/env_$DATE

# Keep only last 7 days
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "env_*" -mtime +7 -delete
EOF

chmod +x /usr/local/bin/backup-platform

# Add to crontab (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/backup-platform") | crontab -
```

### 5. Set Up Monitoring

```bash
# Install monitoring tools
apt-get install -y htop iotop nethogs

# Create monitoring script
cat > /usr/local/bin/monitor-platform <<'EOF'
#!/bin/bash
echo "=== Docker Containers ==="
docker-compose -f /opt/coding-platform/docker-compose.yml ps
echo ""
echo "=== Resource Usage ==="
docker stats --no-stream
echo ""
echo "=== Recent Logs ==="
docker-compose -f /opt/coding-platform/docker-compose.yml logs --tail=20
EOF

chmod +x /usr/local/bin/monitor-platform
```

## Maintenance

### Regular Updates

```bash
# Update system packages
apt-get update && apt-get upgrade -y

# Update Docker images
cd /opt/coding-platform
docker-compose pull
docker-compose up -d
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
docker-compose restart nginx
```

### Update Application

```bash
cd /opt/coding-platform
git pull
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Troubleshooting

### Services Not Starting

```bash
# Check Docker is running
systemctl status docker

# Check for port conflicts
netstat -tulpn | grep -E ':(80|443|3000|8000|5432|6379)'

# Check logs for errors
docker-compose logs
```

### Out of Memory

```bash
# Check memory usage
free -h
docker stats

# Add swap if needed
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

### Database Issues

```bash
# Check PostgreSQL container
docker-compose ps postgres

# Access database
docker exec -it coding_platform_db psql -U platform_user -d coding_platform

# Reset database (⚠️ WARNING: Deletes all data)
docker-compose down -v
docker-compose up -d
docker exec -it coding_platform_backend python database/seed_lessons.py
```

### SSL Certificate Issues

```bash
# Check certificate
openssl x509 -in /opt/coding-platform/nginx/ssl/cert.pem -text -noout

# Renew Let's Encrypt certificate
certbot renew --force-renewal
docker-compose restart nginx
```

### Performance Issues

```bash
# Monitor resources
htop
iotop
nethogs

# Check Docker stats
docker stats

# Increase container resources in docker-compose.yml
# Then restart:
docker-compose up -d
```

## Performance Targets

With CX32 server (4 vCPUs, 8 GB RAM):
- ✓ 10-20 concurrent users
- ✓ Code execution < 2 seconds
- ✓ Page load time < 1 second
- ✓ 99.9% uptime

## Cost Estimation

**Hetzner CX32 Server**:
- Monthly: €11.90
- Annually: €142.80

**Additional Costs**:
- Domain name: $10-15/year
- Backups: €3.20/month (optional)
- Load balancer: €5.20/month (for high availability)

**Total**: ~€15-20/month for production deployment

## Security Checklist

- ✓ Firewall configured (UFW + Hetzner Firewall)
- ✓ SSH key authentication enabled
- ✓ Root login disabled
- ✓ Fail2Ban installed
- ✓ Automatic security updates enabled
- ✓ SSL/TLS certificate installed
- ✓ Docker containers run as non-root
- ✓ Environment variables secured
- ✓ Database password changed from default
- ✓ Rate limiting configured
- ✓ CORS properly configured
- ✓ Regular backups scheduled

## Support

For deployment issues:
- Check logs: `docker-compose logs`
- Review this guide
- Check GitHub issues
- Contact: admin@example.com

## Additional Resources

- [Hetzner Cloud Docs](https://docs.hetzner.com/cloud/)
- [Docker Documentation](https://docs.docker.com/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
