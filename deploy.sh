#!/bin/bash
# ============================================================
# GDU-CTF Lab — Deploy Script for Google Cloud VM
# Run this script on the gdu-ctf-server VM
# ============================================================

set -e

echo "======================================"
echo " GDU-CTF Lab — Deployment Script"
echo "======================================"

REPO_URL="https://github.com/CrisDevil222/gdu-ctf-lab"
APP_DIR="$HOME/gdu-ctf-lab"

# ── 1. Install Docker & Docker Compose (if not already installed) ──
if ! command -v docker &> /dev/null; then
    echo "[*] Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER
    echo "[+] Docker installed. You may need to log out and back in."
fi

if ! docker compose version &> /dev/null; then
    echo "[*] Installing Docker Compose plugin..."
    sudo apt-get install -y docker-compose-plugin
fi

echo "[+] Docker version: $(docker --version)"
echo "[+] Docker Compose version: $(docker compose version)"

# ── 2. Clone or pull latest code ──
if [ -d "$APP_DIR/.git" ]; then
    echo "[*] Pulling latest code from GitHub..."
    cd "$APP_DIR"
    git pull origin main
else
    echo "[*] Cloning repository..."
    sudo git clone "$REPO_URL" "$APP_DIR"
    sudo chown -R $USER:$USER "$APP_DIR"
    cd "$APP_DIR"
fi

echo "[+] Code is up to date."

# ── 3. Build & Start all containers ──
echo "[*] Building Docker images (this may take a few minutes)..."
docker compose build

echo "[*] Starting all services..."
docker compose up -d

echo ""
echo "======================================"
echo " Deployment complete!"
echo "======================================"
docker compose ps
echo ""
echo "Access URLs:"
echo "  Landing page : http://$(curl -s ifconfig.me):5000"
echo "  CTFd Platform: http://$(curl -s ifconfig.me):8000"
echo "  SQLi Easy    : http://$(curl -s ifconfig.me):5001"
echo "  XSS Easy     : http://$(curl -s ifconfig.me):5002"
echo "  IDOR Medium  : http://$(curl -s ifconfig.me):5003"
echo "  SSTI Hard    : http://$(curl -s ifconfig.me):5004"
echo "  Path Traversal: http://$(curl -s ifconfig.me):5005"
echo "  SQLi Medium  : http://$(curl -s ifconfig.me):5006"
echo "  SSRF Medium  : http://$(curl -s ifconfig.me):5007"
