#!/bin/bash

###############################################################################
# Security Hardening Script for Coding Platform
# This script implements security best practices for Ubuntu 22.04 LTS
###############################################################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    log_error "This script must be run as root"
    exit 1
fi

log_info "Starting security hardening..."

###############################################################################
# 1. System Updates
###############################################################################
log_info "Updating system packages..."
apt-get update -qq
apt-get upgrade -y -qq
apt-get autoremove -y -qq
apt-get autoclean -y -qq

###############################################################################
# 2. Firewall Configuration (UFW)
###############################################################################
log_info "Configuring firewall..."

# Install UFW if not installed
apt-get install -y ufw -qq

# Reset UFW to default
ufw --force reset

# Default policies
ufw default deny incoming
ufw default allow outgoing

# Allow SSH (be careful with this!)
ufw allow 22/tcp comment 'SSH'

# Allow HTTP and HTTPS
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'

# Enable UFW
ufw --force enable

log_info "Firewall configured successfully"

###############################################################################
# 3. SSH Hardening
###############################################################################
log_info "Hardening SSH configuration..."

SSH_CONFIG="/etc/ssh/sshd_config"

# Backup original config
cp $SSH_CONFIG ${SSH_CONFIG}.backup

# Disable root login
sed -i 's/^#*PermitRootLogin.*/PermitRootLogin no/' $SSH_CONFIG

# Disable password authentication (enable only if you have SSH keys configured)
# sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' $SSH_CONFIG

# Disable empty passwords
sed -i 's/^#*PermitEmptyPasswords.*/PermitEmptyPasswords no/' $SSH_CONFIG

# Use only SSH Protocol 2
echo "Protocol 2" >> $SSH_CONFIG

# Limit max authentication attempts
sed -i 's/^#*MaxAuthTries.*/MaxAuthTries 3/' $SSH_CONFIG

# Set login grace time
sed -i 's/^#*LoginGraceTime.*/LoginGraceTime 20/' $SSH_CONFIG

# Restart SSH service
systemctl restart sshd

log_info "SSH hardening completed"

###############################################################################
# 4. Fail2Ban Installation
###############################################################################
log_info "Installing and configuring Fail2Ban..."

apt-get install -y fail2ban -qq

# Create custom fail2ban configuration
cat > /etc/fail2ban/jail.local <<EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5
destemail = root@localhost
sendername = Fail2Ban
action = %(action_mwl)s

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3

[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log

[nginx-limit-req]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 10
EOF

# Start and enable Fail2Ban
systemctl enable fail2ban
systemctl restart fail2ban

log_info "Fail2Ban configured successfully"

###############################################################################
# 5. Kernel Hardening (sysctl)
###############################################################################
log_info "Applying kernel security parameters..."

cat > /etc/sysctl.d/99-security.conf <<EOF
# IP Forwarding
net.ipv4.ip_forward = 0

# SYN cookies
net.ipv4.tcp_syncookies = 1

# Ignore ICMP redirects
net.ipv4.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0

# Ignore send redirects
net.ipv4.conf.all.send_redirects = 0

# Disable source packet routing
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0

# Log Martians
net.ipv4.conf.all.log_martians = 1

# Ignore ICMP ping requests
net.ipv4.icmp_echo_ignore_all = 0

# Ignore Broadcast Request
net.ipv4.icmp_echo_ignore_broadcasts = 1

# Increase system file descriptor limit
fs.file-max = 65535

# Allow for more PIDs
kernel.pid_max = 65536

# Increase ephemeral IP ports
net.ipv4.ip_local_port_range = 2000 65000

# Increase TCP max buffer size
net.core.rmem_max = 8388608
net.core.wmem_max = 8388608
net.core.rmem_default = 65536
net.core.wmem_default = 65536
net.ipv4.tcp_rmem = 4096 65536 8388608
net.ipv4.tcp_wmem = 4096 65536 8388608
net.ipv4.tcp_mem = 8388608 8388608 8388608

# Increase the maximum amount of option memory buffers
net.core.optmem_max = 8388608

# Increase the tcp-time-wait buckets pool size
net.ipv4.tcp_max_tw_buckets = 1440000

# Protect against tcp time-wait assassination hazards
net.ipv4.tcp_rfc1337 = 1

# Protect against SYN flood attacks
net.ipv4.tcp_max_syn_backlog = 8192
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_syn_retries = 2
EOF

# Apply sysctl changes
sysctl -p /etc/sysctl.d/99-security.conf

log_info "Kernel security parameters applied"

###############################################################################
# 6. Automatic Security Updates
###############################################################################
log_info "Configuring automatic security updates..."

apt-get install -y unattended-upgrades apt-listchanges -qq

# Configure automatic updates
cat > /etc/apt/apt.conf.d/50unattended-upgrades <<EOF
Unattended-Upgrade::Allowed-Origins {
    "\${distro_id}:\${distro_codename}";
    "\${distro_id}:\${distro_codename}-security";
    "\${distro_id}ESMApps:\${distro_codename}-apps-security";
    "\${distro_id}ESM:\${distro_codename}-infra-security";
};
Unattended-Upgrade::AutoFixInterruptedDpkg "true";
Unattended-Upgrade::MinimalSteps "true";
Unattended-Upgrade::Remove-Unused-Kernel-Packages "true";
Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::Automatic-Reboot "false";
Unattended-Upgrade::Automatic-Reboot-Time "02:00";
EOF

# Enable automatic updates
cat > /etc/apt/apt.conf.d/20auto-upgrades <<EOF
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::AutocleanInterval "7";
APT::Periodic::Unattended-Upgrade "1";
EOF

log_info "Automatic security updates configured"

###############################################################################
# 7. Docker Security
###############################################################################
log_info "Applying Docker security configurations..."

# Create Docker daemon configuration for security
mkdir -p /etc/docker

cat > /etc/docker/daemon.json <<EOF
{
  "live-restore": true,
  "userland-proxy": false,
  "no-new-privileges": true,
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "default-ulimits": {
    "nofile": {
      "Name": "nofile",
      "Hard": 64000,
      "Soft": 64000
    }
  }
}
EOF

# Restart Docker if it's running
if systemctl is-active --quiet docker; then
    systemctl restart docker
    log_info "Docker daemon restarted with security configurations"
fi

###############################################################################
# 8. File Permissions
###############################################################################
log_info "Setting secure file permissions..."

# Secure /etc/passwd and /etc/shadow
chmod 644 /etc/passwd
chmod 600 /etc/shadow
chmod 644 /etc/group
chmod 600 /etc/gshadow

# Secure SSH directory
if [ -d /root/.ssh ]; then
    chmod 700 /root/.ssh
    chmod 600 /root/.ssh/* 2>/dev/null || true
fi

log_info "File permissions secured"

###############################################################################
# 9. Install Security Tools
###############################################################################
log_info "Installing security monitoring tools..."

apt-get install -y \
    aide \
    rkhunter \
    chkrootkit \
    logwatch \
    -qq

# Initialize AIDE database (this may take a while)
log_info "Initializing AIDE database (this may take several minutes)..."
aideinit &

log_info "Security tools installed"

###############################################################################
# 10. Swap Configuration (for 4GB RAM server)
###############################################################################
log_info "Configuring swap space..."

# Check if swap already exists
if [ $(swapon --show | wc -l) -eq 0 ]; then
    # Create 2GB swap file
    fallocate -l 2G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile

    # Make swap permanent
    echo '/swapfile none swap sw 0 0' | tee -a /etc/fstab

    # Optimize swap usage
    sysctl vm.swappiness=10
    echo 'vm.swappiness=10' >> /etc/sysctl.conf

    log_info "Swap configured successfully"
else
    log_info "Swap already configured, skipping..."
fi

###############################################################################
# Summary
###############################################################################
echo ""
echo "========================================="
log_info "Security hardening completed!"
echo "========================================="
echo ""
echo "Applied configurations:"
echo "  ✓ System updates"
echo "  ✓ Firewall (UFW) configured"
echo "  ✓ SSH hardened"
echo "  ✓ Fail2Ban installed"
echo "  ✓ Kernel parameters hardened"
echo "  ✓ Automatic security updates enabled"
echo "  ✓ Docker security configured"
echo "  ✓ File permissions secured"
echo "  ✓ Security tools installed"
echo "  ✓ Swap space configured"
echo ""
log_warn "Please review and test the configurations!"
log_warn "SSH root login has been disabled."
echo ""
