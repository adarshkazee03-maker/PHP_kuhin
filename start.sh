#!/bin/bash

# KUHIN Website - macOS Startup Script

echo "========================================="
echo "   KUHIN WEBSITE - STARTUP"
echo "========================================="
echo ""

# Navigate to project directory
cd "$(dirname "$0")"

# Activate virtual environment
echo "1. Activating virtual environment..."
source venv/bin/activate

# Check for database
if [ ! -f "db.sqlite3" ]; then
    echo ""
    echo "2. Database not found, creating..."
    python manage.py migrate
else
    echo "2. Database found, skipping migration..."
fi

# Start the development server
echo ""
echo "========================================="
echo "   Starting Development Server"
echo "========================================="
echo ""
echo "🚀 Server running at: http://127.0.0.1:8000"
echo "📊 Admin panel at: http://127.0.0.1:8000/admin"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================="
echo ""

python manage.py runserver
