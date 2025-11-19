#!/bin/bash

###############################################################################
# Setup Script for Coding Education Platform
# Installs dependencies and prepares the server
###############################################################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    log_error "This script must be run as root (use sudo)"
    exit 1
fi

echo "========================================="
echo "  Coding Platform Setup"
echo "========================================="
echo ""

###############################################################################
# 1. System Updates
###############################################################################
log_step "Step 1: Updating system packages..."
apt-get update -qq
apt-get upgrade -y -qq
log_info "System packages updated"

###############################################################################
# 2. Install Required Packages
###############################################################################
log_step "Step 2: Installing required packages..."
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git \
    ufw \
    certbot \
    python3-certbot-nginx \
    -qq

log_info "Required packages installed"

###############################################################################
# 3. Install Docker
###############################################################################
log_step "Step 3: Installing Docker..."

# Check if Docker is already installed
if command -v docker &> /dev/null; then
    log_info "Docker is already installed"
else
    # Add Docker's official GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    # Set up Docker repository
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

    # Install Docker Engine
    apt-get update -qq
    apt-get install -y docker-ce docker-ce-cli containerd.io -qq

    # Start and enable Docker
    systemctl start docker
    systemctl enable docker

    log_info "Docker installed successfully"
fi

###############################################################################
# 4. Install Docker Compose
###############################################################################
log_step "Step 4: Installing Docker Compose..."

# Check if Docker Compose is already installed
if command -v docker-compose &> /dev/null; then
    log_info "Docker Compose is already installed"
else
    # Install Docker Compose
    DOCKER_COMPOSE_VERSION="2.23.0"
    curl -SL "https://github.com/docker/compose/releases/download/v${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" \
        -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose

    # Create symlink
    ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose

    log_info "Docker Compose installed successfully"
fi

###############################################################################
# 5. Configure Docker for non-root user (optional)
###############################################################################
log_step "Step 5: Configuring Docker permissions..."

# Create docker group if it doesn't exist
if ! getent group docker > /dev/null; then
    groupadd docker
fi

# Add current user to docker group (if not root)
if [ -n "${SUDO_USER:-}" ]; then
    usermod -aG docker $SUDO_USER
    log_info "User $SUDO_USER added to docker group"
    log_warn "Please log out and back in for group changes to take effect"
fi

###############################################################################
# 6. Create Application Directory
###############################################################################
log_step "Step 6: Setting up application directory..."

APP_DIR="/opt/coding-platform"

if [ -d "$APP_DIR" ]; then
    log_warn "Application directory already exists at $APP_DIR"
else
    mkdir -p $APP_DIR
    log_info "Application directory created at $APP_DIR"
fi

###############################################################################
# 7. Set up Logging
###############################################################################
log_step "Step 7: Setting up logging directories..."

mkdir -p $APP_DIR/logs
mkdir -p /var/log/coding-platform

# Create log rotation configuration
cat > /etc/logrotate.d/coding-platform <<EOF
/var/log/coding-platform/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 root root
    sharedscripts
}
EOF

log_info "Logging configured"

###############################################################################
# 8. Configure Firewall
###############################################################################
log_step "Step 8: Configuring firewall..."

# Check if UFW is active
if ufw status | grep -q "Status: active"; then
    log_info "UFW is already configured"
else
    ufw --force reset
    ufw default deny incoming
    ufw default allow outgoing
    ufw allow 22/tcp comment 'SSH'
    ufw allow 80/tcp comment 'HTTP'
    ufw allow 443/tcp comment 'HTTPS'
    ufw --force enable
    log_info "Firewall configured"
fi

###############################################################################
# 9. Generate Self-Signed SSL Certificate (for development)
###############################################################################
log_step "Step 9: Generating self-signed SSL certificate..."

SSL_DIR="$APP_DIR/nginx/ssl"
mkdir -p $SSL_DIR

if [ ! -f "$SSL_DIR/cert.pem" ]; then
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout $SSL_DIR/key.pem \
        -out $SSL_DIR/cert.pem \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

    log_info "Self-signed SSL certificate generated"
    log_warn "This is a self-signed certificate. Use Let's Encrypt for production!"
else
    log_info "SSL certificate already exists"
fi

###############################################################################
# 10. Create Backup Directory
###############################################################################
log_step "Step 10: Setting up backup directory..."

BACKUP_DIR="/var/backups/coding-platform"
mkdir -p $BACKUP_DIR

# Create backup script
cat > /usr/local/bin/backup-coding-platform <<'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/coding-platform"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$DATE.tar.gz"

# Backup database
docker exec coding_platform_db pg_dump -U platform_user coding_platform > $BACKUP_DIR/db_$DATE.sql

# Backup .env file
cp /opt/coding-platform/.env $BACKUP_DIR/env_$DATE

# Create compressed archive
tar -czf $BACKUP_FILE -C /opt/coding-platform .env

# Keep only last 7 days of backups
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +7 -delete
find $BACKUP_DIR -name "db_*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "env_*" -mtime +7 -delete

echo "Backup completed: $BACKUP_FILE"
EOF

chmod +x /usr/local/bin/backup-coding-platform

# Create cron job for daily backups at 2 AM
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/backup-coding-platform >> /var/log/coding-platform/backup.log 2>&1") | crontab -

log_info "Backup system configured"

###############################################################################
# 11. System Optimization
###############################################################################
log_step "Step 11: Applying system optimizations..."

# Increase file descriptor limits
cat >> /etc/security/limits.conf <<EOF
* soft nofile 65536
* hard nofile 65536
root soft nofile 65536
root hard nofile 65536
EOF

# Increase inotify watchers (for file watching)
echo "fs.inotify.max_user_watches=524288" >> /etc/sysctl.conf
sysctl -p

log_info "System optimizations applied"

###############################################################################
# 12. Install Monitoring Tools (optional)
###############################################################################
log_step "Step 12: Installing monitoring tools..."

apt-get install -y htop iotop nethogs -qq

log_info "Monitoring tools installed"

###############################################################################
# Summary
###############################################################################
echo ""
echo "========================================="
log_info "Setup completed successfully!"
echo "========================================="
echo ""
echo "Installation summary:"
echo "  ✓ System packages updated"
echo "  ✓ Docker installed"
echo "  ✓ Docker Compose installed"
echo "  ✓ Application directory: $APP_DIR"
echo "  ✓ Firewall configured"
echo "  ✓ SSL certificate generated"
echo "  ✓ Backup system configured"
echo "  ✓ System optimizations applied"
echo "  ✓ Monitoring tools installed"
echo ""
echo "Next steps:"
echo "  1. Copy your application files to $APP_DIR"
echo "  2. Configure .env file with production values"
echo "  3. Run: cd $APP_DIR && docker-compose up -d"
echo "  4. For SSL: certbot --nginx -d yourdomain.com"
echo "  5. Run security hardening: ./deployment/security-hardening.sh"
echo ""
log_warn "Please review all configurations before deploying to production!"
echo ""
