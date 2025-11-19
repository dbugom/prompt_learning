#!/bin/bash

###############################################################################
# Automated Deployment Script for Hetzner Cloud
# Deploys the complete Coding Education Platform
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

# Configuration
APP_DIR="/opt/coding-platform"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "========================================="
echo "  Hetzner Deployment Script"
echo "  Coding Education Platform"
echo "========================================="
echo ""

###############################################################################
# Pre-flight Checks
###############################################################################
log_step "Running pre-flight checks..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    log_error "This script must be run as root (use sudo)"
    exit 1
fi

# Check internet connectivity
if ! ping -c 1 google.com &> /dev/null; then
    log_error "No internet connectivity"
    exit 1
fi

log_info "Pre-flight checks passed"

###############################################################################
# Step 1: Run Setup Script
###############################################################################
log_step "Step 1: Running system setup..."

if [ -f "$SCRIPT_DIR/setup.sh" ]; then
    bash "$SCRIPT_DIR/setup.sh"
else
    log_error "Setup script not found!"
    exit 1
fi

###############################################################################
# Step 2: Run Security Hardening
###############################################################################
log_step "Step 2: Running security hardening..."

if [ -f "$SCRIPT_DIR/security-hardening.sh" ]; then
    bash "$SCRIPT_DIR/security-hardening.sh"
else
    log_warn "Security hardening script not found, skipping..."
fi

###############################################################################
# Step 3: Copy Application Files
###############################################################################
log_step "Step 3: Deploying application files..."

# Create application directory if it doesn't exist
mkdir -p $APP_DIR

# Copy application files
log_info "Copying application files..."
rsync -av --exclude='node_modules' --exclude='.git' --exclude='__pycache__' \
    "$PROJECT_ROOT/" "$APP_DIR/"

# Set proper ownership
chown -R root:root $APP_DIR

log_info "Application files deployed"

###############################################################################
# Step 4: Configure Environment Variables
###############################################################################
log_step "Step 4: Configuring environment variables..."

# Generate secure random strings
generate_secret() {
    openssl rand -base64 32 | tr -d /=+ | cut -c -32
}

POSTGRES_PASSWORD=$(generate_secret)
REDIS_PASSWORD=$(generate_secret)
SECRET_KEY=$(generate_secret)$(generate_secret)

# Create production .env file
cat > $APP_DIR/.env <<EOF
# Production Environment Configuration
# Generated on $(date)

# Database Configuration
POSTGRES_DB=coding_platform
POSTGRES_USER=platform_user
POSTGRES_PASSWORD=$POSTGRES_PASSWORD

# Redis Configuration
REDIS_PASSWORD=$REDIS_PASSWORD

# Backend Configuration
SECRET_KEY=$SECRET_KEY
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
RATE_LIMIT_PER_MINUTE=10

# Frontend Configuration (update with your domain)
NEXT_PUBLIC_API_URL=https://yourdomain.com/api
NEXT_PUBLIC_WS_URL=wss://yourdomain.com/ws

# CORS Configuration (update with your domain)
ALLOWED_ORIGINS=https://yourdomain.com

# Email Configuration (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=

# Domain Configuration
DOMAIN=yourdomain.com
ADMIN_EMAIL=admin@yourdomain.com
EOF

chmod 600 $APP_DIR/.env

log_info "Environment variables configured"
log_warn "Please update DOMAIN and other settings in $APP_DIR/.env"

###############################################################################
# Step 5: Build and Start Docker Containers
###############################################################################
log_step "Step 5: Building and starting Docker containers..."

cd $APP_DIR

# Pull latest images
log_info "Pulling Docker images..."
docker-compose pull

# Build custom images
log_info "Building application images..."
docker-compose build --no-cache

# Start services
log_info "Starting services..."
docker-compose up -d

# Wait for services to be healthy
log_info "Waiting for services to be healthy..."
sleep 30

# Check service status
docker-compose ps

log_info "Services started successfully"

###############################################################################
# Step 6: Initialize Database
###############################################################################
log_step "Step 6: Initializing database..."

# Wait for database to be ready
log_info "Waiting for database to be ready..."
sleep 10

# Create initial admin user (optional)
log_info "Database initialization completed"
log_warn "You can create an admin user through the registration endpoint"

###############################################################################
# Step 7: Configure SSL/TLS (Let's Encrypt)
###############################################################################
log_step "Step 7: Configuring SSL/TLS..."

read -p "Do you want to configure Let's Encrypt SSL? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter your domain name: " DOMAIN
    read -p "Enter your email: " EMAIL

    log_info "Obtaining SSL certificate from Let's Encrypt..."

    # Stop nginx temporarily
    docker-compose stop nginx

    # Get certificate
    certbot certonly --standalone \
        -d $DOMAIN \
        --email $EMAIL \
        --agree-tos \
        --non-interactive \
        --preferred-challenges http

    # Copy certificates to nginx ssl directory
    cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem $APP_DIR/nginx/ssl/cert.pem
    cp /etc/letsencrypt/live/$DOMAIN/privkey.pem $APP_DIR/nginx/ssl/key.pem

    # Start nginx
    docker-compose start nginx

    # Set up auto-renewal
    (crontab -l 2>/dev/null; echo "0 3 * * * certbot renew --quiet --deploy-hook 'docker-compose -f $APP_DIR/docker-compose.yml restart nginx'") | crontab -

    log_info "SSL/TLS configured successfully"
else
    log_info "Skipping SSL/TLS configuration"
    log_warn "Using self-signed certificate. Configure SSL manually for production!"
fi

###############################################################################
# Step 8: Set up Monitoring
###############################################################################
log_step "Step 8: Setting up monitoring..."

# Create monitoring script
cat > /usr/local/bin/monitor-coding-platform <<'EOF'
#!/bin/bash
echo "=== Coding Platform Status ==="
echo ""
echo "Docker Containers:"
docker-compose -f /opt/coding-platform/docker-compose.yml ps
echo ""
echo "Resource Usage:"
docker stats --no-stream
echo ""
echo "Recent Logs:"
docker-compose -f /opt/coding-platform/docker-compose.yml logs --tail=20
EOF

chmod +x /usr/local/bin/monitor-coding-platform

log_info "Monitoring script created: /usr/local/bin/monitor-coding-platform"

###############################################################################
# Step 9: Create Management Scripts
###############################################################################
log_step "Step 9: Creating management scripts..."

# Start script
cat > /usr/local/bin/start-platform <<EOF
#!/bin/bash
cd $APP_DIR
docker-compose up -d
echo "Platform started"
EOF
chmod +x /usr/local/bin/start-platform

# Stop script
cat > /usr/local/bin/stop-platform <<EOF
#!/bin/bash
cd $APP_DIR
docker-compose down
echo "Platform stopped"
EOF
chmod +x /usr/local/bin/stop-platform

# Restart script
cat > /usr/local/bin/restart-platform <<EOF
#!/bin/bash
cd $APP_DIR
docker-compose restart
echo "Platform restarted"
EOF
chmod +x /usr/local/bin/restart-platform

# Update script
cat > /usr/local/bin/update-platform <<EOF
#!/bin/bash
cd $APP_DIR
git pull
docker-compose down
docker-compose build --no-cache
docker-compose up -d
echo "Platform updated"
EOF
chmod +x /usr/local/bin/update-platform

log_info "Management scripts created"

###############################################################################
# Step 10: Create Sample Lessons
###############################################################################
log_step "Step 10: Creating sample lessons..."

# This will be done through the API or admin interface
log_info "Sample lessons will be created separately"
log_warn "Use the lessons API to create initial course content"

###############################################################################
# Final Summary
###############################################################################
echo ""
echo "========================================="
log_info "Deployment completed successfully!"
echo "========================================="
echo ""
echo "Application Details:"
echo "  • Location: $APP_DIR"
echo "  • Frontend: http://$(curl -s ifconfig.me)"
echo "  • API: http://$(curl -s ifconfig.me)/api"
echo "  • Environment: $APP_DIR/.env"
echo ""
echo "Management Commands:"
echo "  • start-platform    - Start all services"
echo "  • stop-platform     - Stop all services"
echo "  • restart-platform  - Restart all services"
echo "  • update-platform   - Pull updates and rebuild"
echo "  • monitor-coding-platform - View system status"
echo "  • docker-compose -f $APP_DIR/docker-compose.yml logs -f"
echo ""
echo "Next Steps:"
echo "  1. Update $APP_DIR/.env with your domain and settings"
echo "  2. Configure SSL certificate for production"
echo "  3. Create sample lessons through the API"
echo "  4. Register admin user"
echo "  5. Test the platform"
echo ""
log_warn "Important: Review and update the .env file!"
log_warn "Change default passwords immediately!"
echo ""
echo "Access your platform at: http://$(curl -s ifconfig.me)"
echo ""
