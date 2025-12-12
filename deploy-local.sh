#!/bin/bash

# Multi-Agent Food Ordering System - Local Deployment Script
# This script deploys the application locally using docker-compose

set -e

echo "🚀 Starting Local Deployment..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  Warning: .env file not found. Copying from .env.example...${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${YELLOW}Please edit .env file with your API keys before proceeding.${NC}"
        exit 1
    else
        echo "Error: .env.example not found either!"
        exit 1
    fi
fi

# Determine environment
ENVIRONMENT=${1:-production}

echo "Environment: $ENVIRONMENT"

# Stop and remove old containers
echo "🛑 Stopping existing containers..."
if [ "$ENVIRONMENT" == "staging" ]; then
    docker-compose -f docker-compose.staging.yml down || true
else
    docker-compose down || true
fi

# Deploy services
echo "📦 Starting services..."
if [ "$ENVIRONMENT" == "staging" ]; then
    docker-compose -f docker-compose.staging.yml up -d
    echo -e "${GREEN}✅ Staging deployment complete!${NC}"
    echo ""
    echo "Access your application at:"
    echo "  - Frontend: http://localhost:8080"
    echo "  - Backend:  http://localhost:8006"
else
    docker-compose up -d
    echo -e "${GREEN}✅ Production deployment complete!${NC}"
    echo ""
    echo "Access your application at:"
    echo "  - Frontend: http://localhost"
    echo "  - Backend:  http://localhost:8005"
fi

# Show running containers
echo ""
echo "Running containers:"
docker ps --filter "name=food-ordering"

echo ""
echo "📝 View logs with: docker-compose logs -f"
echo "🛑 Stop with: docker-compose down"
