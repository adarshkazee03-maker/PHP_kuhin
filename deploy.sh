#!/bin/bash
# KUHIN Deployment Script
# Run this script on your server to deploy the latest code

set -e

echo "🚀 Starting KUHIN deployment..."

# Navigate to project directory
cd /home/kuhin/kuhin

# Pull latest code from main branch
echo "📥 Pulling latest code from git..."
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --settings=kuhin_project.settings.prod

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --no-input --settings=kuhin_project.settings.prod

# Restart Django service
echo "🔄 Restarting KUHIN service..."
sudo systemctl restart kuhin

# Check service status
if sudo systemctl is-active --quiet kuhin; then
    echo "✅ Deployment successful! KUHIN is running."
    echo "🌐 Service status: $(sudo systemctl status kuhin --no-pager | grep Active)"
else
    echo "❌ Deployment failed! KUHIN service is not running."
    echo "🔹 Check logs: sudo journalctl -u kuhin -n 50"
    exit 1
fi
