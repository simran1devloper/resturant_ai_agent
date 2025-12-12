# Multi-Agent Food Ordering System

A modern food ordering system powered by AI agents with RAG (Retrieval Augmented Generation) capabilities.

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd MULti_agent_system

# Copy environment variables
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8005
- API Docs: http://localhost:8005/docs

### Local Development

#### Backend
```bash
cd Backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Build RAG index
python Rag/build_index.py

# Start server
python main.py
```

#### Frontend
```bash
cd Frontend
npm install
npm run dev
```

## 📁 Project Structure

```
MULti_agent_system/
├── Backend/
│   ├── api/              # FastAPI routes
│   ├── agents/           # AI agent configuration
│   ├── Rag/              # RAG knowledge base
│   ├── services/         # Business logic
│   └── Dockerfile
├── Frontend/
│   ├── src/              # React components
│   ├── nginx.conf        # Production nginx config
│   └── Dockerfile
├── .github/
│   └── workflows/        # CI/CD pipelines
├── docker-compose.yml
└── .env.example
```

## 🔬 Testing

### Backend Tests
```bash
cd Backend
pytest --cov=. --cov-report=html
```

### Frontend Tests
```bash
cd Frontend
npm test
```

## 🚢 Deployment

### Docker

Build and push images:
```bash
docker build -t your-registry/backend:latest ./Backend
docker build -t your-registry/frontend:latest ./Frontend

docker push your-registry/backend:latest
docker push your-registry/frontend:latest
```

### With MLOps Stack

Start with monitoring and experiment tracking:
```bash
docker-compose --profile mlops --profile monitoring up -d
```

This includes:
- MLflow (http://localhost:5000) - Experiment tracking
- Prometheus (http://localhost:9090) - Metrics
- Grafana (http://localhost:3001) - Visualization

## 🛠️ Development

### Code Quality

```bash
# Backend
black Backend/
flake8 Backend/ --max-line-length=100
isort Backend/

# Frontend
cd Frontend
npm run lint
npx prettier --write "src/**/*.{js,jsx}"
```

### Adding Menu Items

1. Edit `Backend/Rag/menu.json`
2. Rebuild the RAG index:
```bash
cd Backend
python Rag/build_index.py
```

## 🔐 Environment Variables

See `.env.example` for all available configuration options.

Required variables:
- `OPENROUTER_API_KEY` - Your OpenRouter API key

## 📊 Monitoring

Health check endpoints:
- `/health` - Basic health check
- `/readiness` - Service readiness check
- `/liveness` - Liveness probe

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

## 📝 License

[Your License Here]

## 🙏 Acknowledgments

- Built with [agno](https://agno.com) AI framework
- Powered by OpenRouter API
- UI components from Lucide React
