#!/bin/bash

# Quick Docker Test Script
# This script builds and tests the Docker setup

set -e

echo "🧪 Quick Docker Test"
echo "===================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Step 1: Build
echo -e "${BLUE}Step 1: Building Docker images...${NC}"
docker-compose build

echo ""
echo -e "${GREEN}✓ Build complete${NC}"

# Step 2: Start services
echo ""
echo -e "${BLUE}Step 2: Starting services...${NC}"
docker-compose up -d

echo ""
echo -e "${YELLOW}Waiting for services to be healthy (30 seconds)...${NC}"
sleep 30

# Step 3: Check status
echo ""
echo -e "${BLUE}Step 3: Checking service status...${NC}"
docker-compose ps

# Step 4: Test health endpoints
echo ""
echo -e "${BLUE}Step 4: Testing health endpoints...${NC}"

if curl -f http://localhost:8005/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend health check passed${NC}"
    curl http://localhost:8005/health | python3 -m json.tool
else
    echo -e "${RED}✗ Backend health check failed${NC}"
fi

echo ""
if curl -f http://localhost:8005/readiness > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend readiness check passed${NC}"
else
    echo -e "${RED}✗ Backend readiness check failed${NC}"
fi

# Step 5: Test API
echo ""
echo -e "${BLUE}Step 5: Testing RAG API...${NC}"
if curl -f "http://localhost:8005/rag/query?q=show%20pizzas" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ RAG API responding${NC}"
else
    echo -e "${RED}✗ RAG API not responding${NC}"
fi

# Step 6: Show logs
echo ""
echo -e "${BLUE}Step 6: Recent logs (last 20 lines)${NC}"
echo "Backend logs:"
docker-compose logs --tail=20 backend

# Final summary
echo ""
echo "======================================"
echo -e "${GREEN}Docker Test Complete!${NC}"
echo "======================================"
echo ""
echo "Access your services:"
echo "  Frontend:  http://localhost:3000"
echo "  Backend:   http://localhost:8005"
echo "  API Docs:  http://localhost:8005/docs"
echo ""
echo "Useful commands:"
echo "  View logs:        docker-compose logs -f"
echo "  Stop services:    docker-compose down"
echo "  Restart:          docker-compose restart backend"
echo ""
