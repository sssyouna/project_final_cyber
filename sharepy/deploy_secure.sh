#!/bin/bash
set -e

echo "🔒 SharePy Secure Deployment Script"
echo "===================================="

# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "❌ Docker not installed"; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "❌ Docker Compose not installed"; exit 1; }

# Check .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Copy .env.example to .env and configure with secure values"
    exit 1
fi

# Validate .env has strong secrets
if grep -q "CHANGE_ME" .env; then
    echo "❌ .env still contains CHANGE_ME placeholders!"
    exit 1
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build images
echo "🔨 Building secure images..."
docker-compose build --no-cache

# Start services
echo "🚀 Starting secure services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Run security checks
echo "🔍 Running security validation..."
python3 check_security.py

echo "✅ Secure deployment complete!"
echo "📊 Access application at: https://localhost"