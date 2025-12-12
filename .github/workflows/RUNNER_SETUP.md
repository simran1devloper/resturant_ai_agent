# Self-Hosted GitHub Actions Runner Setup Guide

## Overview

This guide will help you set up a GitHub Actions self-hosted runner on your Linux machine to run CI/CD workflows locally.

## Prerequisites

- Linux machine (Ubuntu/Debian recommended)
- Docker and Docker Compose installed
- Git installed
- GitHub repository access (admin/write permissions)

## Step 1: Navigate to Runner Settings

1. Go to your GitHub repository
2. Click **Settings** → **Actions** → **Runners**
3. Click **New self-hosted runner**

## Step 2: Download and Configure Runner

GitHub will provide you with commands. Follow them, but here's a general guide:

```bash
# Create a folder for the runner
mkdir actions-runner && cd actions-runner

# Download the latest runner package (Linux x64)
curl -o actions-runner-linux-x64-2.319.1.tar.gz -L https://github.com/actions/runner/releases/download/v2.319.1/actions-runner-linux-x64-2.319.1.tar.gz

# Extract the installer
tar xzf ./actions-runner-linux-x64-2.319.1.tar.gz

# Configure the runner
./config.sh --url https://github.com/YOUR_USERNAME/YOUR_REPO --token YOUR_TOKEN
```

**Important:** Replace `YOUR_USERNAME`, `YOUR_REPO`, and `YOUR_TOKEN` with your actual values from the GitHub UI.

## Step 3: Configure Runner

When prompted:
- **Runner name:** Choose a descriptive name (e.g., `local-dev-runner`)
- **Work folder:** Press Enter to use default `_work`
- **Labels:** Add any custom labels or press Enter for default

## Step 4: Install as a Service (Recommended)

To run the runner automatically:

```bash
# Install the service
sudo ./svc.sh install

# Start the service
sudo ./svc.sh start

# Check status
sudo ./svc.sh status
```

## Step 5: Manual Start (Alternative)

If you prefer to run manually:

```bash
./run.sh
```

**Note:** The runner must be running for workflows to execute!

## Step 6: Verify Runner

1. Go back to GitHub → Settings → Actions → Runners
2. You should see your runner listed with a **green dot** (idle status)

## Step 7: Set Up Environment

Create a `.env` file in your project root with required API keys:

```bash
cd /path/to/MULti_agent_system
cp .env.example .env
# Edit .env with your actual API keys
nano .env
```

## Running Workflows

Once the runner is set up:

1. **Push to repository** - Workflows will automatically trigger
2. **Check Actions tab** on GitHub to see workflow runs
3. **Logs** are available both on GitHub and on your local machine

## Local Deployment URLs

After successful deployment:

### Production (main branch):
- **Frontend:** http://localhost
- **Backend:** http://localhost:8005

### Staging (develop branch):
- **Frontend:** http://localhost:8080
- **Backend:** http://localhost:8006

## Managing Deployments

Use the provided deployment script:

```bash
# Deploy production
./deploy-local.sh production

# Deploy staging
./deploy-local.sh staging

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Troubleshooting

### Runner Not Starting

```bash
# Check service status
sudo ./svc.sh status

# View service logs
journalctl -u actions.runner.* -f
```

### Docker Permission Issues

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login again
```

### Workflow Not Triggering

- Ensure runner is online (green dot in GitHub)
- Check workflow file syntax
- Verify branch matches workflow triggers

### Port Conflicts

If ports 80, 8005, 8080, or 8006 are in use:

1. Stop conflicting services
2. Or modify ports in `docker-compose.yml` and `docker-compose.staging.yml`

## Security Considerations

> [!WARNING]
> - Self-hosted runners on **public repositories** can be a security risk
> - Ensure your repository is **private** or carefully review all PRs before they run
> - Never store secrets in code - use `.env` file (gitignored)

## Updating the Runner

```bash
cd actions-runner

# Stop the service
sudo ./svc.sh stop

# Download new version and extract
# ... (follow download steps from GitHub)

# Start the service
sudo ./svc.sh start
```

## Removing the Runner

```bash
# Stop and uninstall service
sudo ./svc.sh stop
sudo ./svc.sh uninstall

# Remove from GitHub
./config.sh remove --token YOUR_TOKEN

# Delete folder
cd ..
rm -rf actions-runner
```

## Additional Resources

- [GitHub Self-Hosted Runners Docs](https://docs.github.com/en/actions/hosting-your-own-runners)
- [Docker Installation](https://docs.docker.com/engine/install/)
- [Docker Compose Installation](https://docs.docker.com/compose/install/)
