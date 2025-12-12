#!/bin/bash

# Quick Test Script for CI/CD Infrastructure
# Run this to test your Docker setup

set -e  # Exit on error

echo "🚀 Testing CI/CD Infrastructure..."
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Docker installed
echo "📋 Test 1: Checking Docker installation..."
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓ Docker installed: $(docker --version)${NC}"
else
    echo -e "${RED}✗ Docker not installed${NC}"
    exit 1
fi

# Test 2: Docker Compose installed
echo ""
echo "📋 Test 2: Checking Docker Compose..."
if command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}✓ Docker Compose installed: $(docker-compose --version)${NC}"
else
    echo -e "${RED}✗ Docker Compose not installed${NC}"
    exit 1
fi

# Test 3: .env file exists
echo ""
echo "📋 Test 3: Checking .env file..."
if [ -f ".env" ]; then
    echo -e "${GREEN}✓ .env file exists${NC}"
    if grep -q "OPENROUTER_API_KEY=sk-" .env; then
        echo -e "${GREEN}✓ API key configured${NC}"
    else
        echo -e "${YELLOW}⚠ API key might not be set properly${NC}"
    fi
else
    echo -e "${RED}✗ .env file missing${NC}"
    echo "Run: cp .env.example .env"
    exit 1
fi

# Test 4: Validate docker-compose.yml
echo ""
echo "📋 Test 4: Validating docker-compose.yml..."
if docker-compose config > /dev/null 2>&1; then
    echo -e "${GREEN}✓ docker-compose.yml is valid${NC}"
else
    echo -e "${RED}✗ docker-compose.yml has errors${NC}"
    exit 1
fi

# Test 5: Check if ports are available
echo ""
echo "📋 Test 5: Checking if ports are available..."
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠ Port $1 is already in use${NC}"
        return 1
    else
        echo -e "${GREEN}✓ Port $1 is available${NC}"
        return 0
    fi
}

check_port 8005  # Backend
check_port 3000  # Frontend

echo ""
echo "======================================"
echo -e "${GREEN}All basic tests passed!${NC}"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Build images:     docker-compose build"
echo "2. Start services:   docker-compose up -d"
echo "3. Check status:     docker-compose ps"
echo "4. View logs:        docker-compose logs -f"
echo "5. Test health:      curl http://localhost:8005/health"
echo "6. Open frontend:    http://localhost:3000"
echo ""
echo "Or run the full test:"
echo "  bash test-docker-quick.sh"
