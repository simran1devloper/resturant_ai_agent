# Testing Guide - CI/CD Infrastructure

## Quick Test Checklist

### ✅ Pre-requisites
- [ ] Docker installed and running
- [ ] Docker Compose installed
- [ ] `.env` file created from `.env.example`
- [ ] OPENROUTER_API_KEY set in `.env`

### ✅ Local Docker Tests
- [ ] Docker Compose configuration valid
- [ ] Backend builds successfully
- [ ] Frontend builds successfully
- [ ] Services start and are healthy
- [ ] Health endpoints respond
- [ ] Frontend can communicate with backend

### ✅ CI/CD Tests (Optional)
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] GitHub Actions workflow runs
- [ ] Tests pass
- [ ] Docker images build

---

## Step-by-Step Testing Instructions

### Step 1: Environment Setup

```bash
# Navigate to project directory
cd /home/sonia/Documents/test/new/MULti_agent_system

# Create .env file from example
cp .env.example .env

# Edit .env and add your OPENROUTER_API_KEY
nano .env  # or use your preferred editor
# Add: OPENROUTER_API_KEY=sk-or-v1-...
```

### Step 2: Validate Docker Configuration

```bash
# Check Docker is running
docker --version
docker-compose --version

# Validate docker-compose.yml syntax
docker-compose config

# Expected: Should show the parsed configuration without errors
```

### Step 3: Build Docker Images

```bash
# Build all images (this may take a few minutes)
docker-compose build

# Expected output:
# - Building backend...
# - Building frontend...
# - Successfully built and tagged images
```

**Watch for**:
- ✅ "Successfully built" for both backend and frontend
- ❌ Any build errors (missing dependencies, syntax errors)

### Step 4: Start Services

```bash
# Start all services in detached mode
docker-compose up -d

# Check service status
docker-compose ps

# Expected: All services should show (healthy) or Up
```

**Expected output**:
```
NAME                        STATUS                   PORTS
food-ordering-backend       Up (healthy)             0.0.0.0:8005->8005/tcp
food-ordering-frontend      Up (healthy)             0.0.0.0:3000->80/tcp
```

### Step 5: View Logs

```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View specific service logs
docker-compose logs backend
docker-compose logs frontend

# Last 50 lines
docker-compose logs --tail=50 backend
```

**Look for**:
- ✅ "Uvicorn running on http://0.0.0.0:8005" (backend)
- ✅ "INFO Embedder..." messages
- ✅ No error messages
- ❌ Import errors or dependency issues

### Step 6: Test Health Endpoints

```bash
# Backend health check
curl http://localhost:8005/health

# Expected response:
# {"status":"healthy","service":"food-ordering-backend","version":"1.0.0"}

# Readiness check
curl http://localhost:8005/readiness

# Liveness check
curl http://localhost:8005/liveness
```

**Or use browser**:
- http://localhost:8005/health
- http://localhost:8005/docs (FastAPI Swagger UI!)

### Step 7: Test API Endpoints

```bash
# Test RAG query endpoint
curl "http://localhost:8005/rag/query?q=Show%20me%20pizzas"

# Test menu endpoint
curl http://localhost:8005/menu/all

# Expected: JSON responses with menu data
```

### Step 8: Test Frontend

Open browser and navigate to:
- **Frontend**: http://localhost:3000
- **Click**: "AI Assistant" tab
- **Try query**: "Show me all pizzas"

**Expected**:
- ✅ App loads without errors
- ✅ Chat interface is visible
- ✅ Query returns formatted menu with emojis and tables
- ✅ Markdown renders properly

### Step 9: Test Full Stack Integration

```bash
# In one terminal, watch backend logs
docker-compose logs -f backend

# In another terminal or browser:
# - Open http://localhost:3000
# - Go to AI Assistant tab
# - Send a message: "What vegetarian dishes do you have?"

# Watch the backend logs for the request
```

**Look for**:
- Request logged in backend
- INFO messages about RAG search
- Response sent back
- Frontend displays formatted response

### Step 10: Test Container Restart

```bash
# Restart a specific service
docker-compose restart backend

# Watch it come back up
docker-compose logs -f backend

# Check health
curl http://localhost:8005/health
```

### Step 11: Clean Up

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (careful!)
docker-compose down -v

# Stop and remove images
docker-compose down --rmi all
```

---

## Testing with MLOps Stack

### Start with MLflow

```bash
# Start backend + frontend + MLflow
docker-compose --profile mlops up -d

# Access MLflow
# Open browser: http://localhost:5000

# Check all services
docker-compose ps
```

**Expected**:
```
food-ordering-backend      Up
food-ordering-frontend     Up
mlflow-server              Up
```

### Start Full Monitoring Stack

```bash
# Start everything
docker-compose --profile mlops --profile monitoring up -d

# Check all services
docker-compose ps

# Access services:
# MLflow: http://localhost:5000
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3001 (admin/admin)
```

---

## Troubleshooting

### Issue: "Service becomes unhealthy"

**Check logs**:
```bash
docker-compose logs backend
```

**Common causes**:
- Missing `.env` file
- Invalid API key
- Port already in use
- Dependency issues

**Fix**:
```bash
# Rebuild without cache
docker-compose build --no-cache backend
docker-compose up -d
```

### Issue: "Cannot connect to backend"

**Check network**:
```bash
# Inspect network
docker network inspect multi_agent_system_app-network

# Check if containers are on same network
docker-compose ps
```

**Fix**:
```bash
docker-compose down
docker-compose up -d
```

### Issue: "Frontend shows connection error"

**Check API proxy**:
1. Open browser console (F12)
2. Look for network errors
3. Check if requests to `/api/` are being proxied

**Verify nginx config**:
```bash
# Access frontend container
docker-compose exec frontend cat /etc/nginx/conf.d/default.conf
```

### Issue: "Import errors in backend"

**Check dependencies**:
```bash
# Verify Python packages installed
docker-compose exec backend pip list

# Rebuild with updated requirements
docker-compose build --no-cache backend
```

---

## Advanced Testing

### Performance Test

```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Test backend endpoint (100 requests, 10 concurrent)
ab -n 100 -c 10 http://localhost:8005/health

# Check response times
```

### Load Test

```bash
# Using hey (install: go install github.com/rakyll/hey@latest)
hey -n 1000 -c 50 http://localhost:8005/health
```

### Memory Usage

```bash
# Check container stats
docker stats

# Expected memory usage:
# backend: ~500MB-1GB
# frontend: ~20-50MB
```

---

## GitHub CI/CD Testing

### Step 1: Initialize Git Repository

```bash
cd /home/sonia/Documents/test/new/MULti_agent_system

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "feat: Add CI/CD infrastructure"
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Create repository (e.g., "food-ordering-system")
3. Don't initialize with README (we have one)

### Step 3: Push to GitHub

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push
git push -u origin main
```

### Step 4: Watch GitHub Actions

1. Go to your repository on GitHub
2. Click "Actions" tab
3. You should see workflows running:
   - "CI/CD Pipeline"
   - "Code Quality"

### Step 5: Check Results

**Expected**:
- ✅ All jobs pass (green checkmarks)
- ✅ Docker images built
- ✅ Tests executed
- ✅ Code quality checks pass

---

## Quick Commands Reference

```bash
# Start everything
docker-compose up -d

# Stop everything
docker-compose down

# Restart a service
docker-compose restart backend

# View logs
docker-compose logs -f

# Rebuild and restart
docker-compose up -d --build

# Check status
docker-compose ps

# Execute command in container
docker-compose exec backend python -c "print('Hello')"

# Scale a service
docker-compose up -d --scale backend=3
```

---

## Success Criteria

### ✅ Basic Setup
- [ ] Docker Compose config is valid
- [ ] All images build without errors
- [ ] Services start successfully
- [ ] Health checks pass

### ✅ Functionality
- [ ] Backend API responds
- [ ] Frontend loads in browser
- [ ] Can query the AI agent
- [ ] Menu data displays correctly
- [ ] Markdown formatting works

### ✅ Integration
- [ ] Frontend can call backend API
- [ ] RAG knowledge base works
- [ ] Agent returns formatted responses
- [ ] No CORS errors

### ✅ CI/CD (if using GitHub)
- [ ] Workflows trigger on push
- [ ] Tests pass
- [ ] Images build
- [ ] Code quality checks pass

---

## Next Steps After Testing

Once everything works:

1. **Development**: Use docker-compose for local development
2. **Testing**: Add pytest tests (Phase 2)
3. **Deployment**: Deploy to cloud platform
4. **Monitoring**: Enable Grafana/Prometheus stack
5. **MLOps**: Track experiments with MLflow

Happy testing! 🚀
