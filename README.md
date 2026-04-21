# Multi-service Job Pipeline

A multi-service job processing application where users can submit jobs through a web dashboard and track them in real time. When a job is submitted, it gets queued in Redis, picked up by a background worker, processed, and the status updates to completed on the dashboard.

This repository is a forked and fixed version of [chukwukelu2023/hng14-stage2-devops](https://github.com/chukwukelu2023/hng14-stage2-devops). The original source code contained bugs and misconfigurations that were identified, fixed, and documented in [FIXES.md](./FIXES.md).


## Architecture

The application is made up of four services that communicate over a shared internal Docker network:

- **Frontend** — Node.js/Express web server on port 3000. Users submit jobs and track their status here.
- **API** — Python/FastAPI service on port 8000. Creates jobs, pushes them to Redis, and serves status updates.
- **Worker** — Python background service. Polls Redis for new jobs, processes them, and updates their status to completed.
- **Redis** — In-memory data store used as both a job queue and a status store. Not exposed outside the internal network.

## Prerequisites

Make sure you have the following installed before you begin:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) — required to build and run all containers
- [Git](https://git-scm.com/) — required to clone the repository
- [Python 3.11+](https://www.python.org/downloads/) — required for local development and linting
- [Node.js v20+](https://nodejs.org/) — required for local frontend development and linting
- [flake8](https://flake8.pycqa.org/) — Python linter (`pip install flake8`)
- [ESLint](https://eslint.org/) — JavaScript linter (`npm install -g eslint`)
- [hadolint](https://github.com/hadolint/hadolint) — Dockerfile linter


## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/job-processing-platform.git
cd job-processing-platform
```

### 2. Create the environment file

Create a `.env` file at the root of the project:

```bash
cp .env.example .env
```

The default values in `.env.example` work out of the box with no changes needed for local development.

### 3. Bring the full stack up

```bash
docker compose up --build
```

This command will:
- Build all three service images from their Dockerfiles
- Pull the Redis Alpine image
- Start all four containers on a shared internal network
- Run health checks before starting dependent services

### 4. Verify the services are healthy

In a separate terminal, run:

```bash
docker compose ps
```

You should see all four services with a `healthy` status:
<img width="1605" height="239" alt="image" src="https://github.com/user-attachments/assets/1f3e865f-6087-4a80-bb3b-f865f1801397" />

## Using the Application

Once all services are healthy, open your browser and go to:
http://localhost:3000/

You will see the Job Processor Dashboard. Click **Submit New Job** to create a new job. The dashboard will show the job ID and poll for its status automatically. Within a few seconds the status will update to `completed`.

A successful run looks like this:
<img width="944" height="575" alt="image" src="https://github.com/user-attachments/assets/3bfa0a1b-29a2-4f92-b1e0-8756bd228635" />

## Stopping the Stack

```bash
docker compose down
```

To also remove volumes:

```bash
docker compose down -v
```

## Running Locally Without Docker

If you want to run the services individually for development:

### API

```bash
cd api
python -m venv venv
source venv/bin/activate  # windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Worker

```bash
cd worker
python -m venv venv
source venv/bin/activate  # windows: venv\Scripts\activate
pip install -r requirements.txt
python worker.py
```

### Frontend

```bash
cd frontend
npm install
node app.js
```

You will also need a local Redis instance running:

```bash
docker run -d -p 6379:6379 redis:alpine
```

## Running the Linters

### Python (flake8)

```bash
flake8 api/main.py worker/worker.py --max-line-length=120
```

### JavaScript (ESLint)

```bash
cd frontend
npx eslint app.js
```

### Dockerfiles (hadolint)

On Linux/Mac:
```bash
docker run --rm -i hadolint/hadolint < api/Dockerfile
docker run --rm -i hadolint/hadolint < worker/Dockerfile
docker run --rm -i hadolint/hadolint < frontend/Dockerfile
```
On Windows Powershell:
```bash
Get-Content api/Dockerfile | docker run --rm -i hadolint/hadolint
Get-Content worker/Dockerfile | docker run --rm -i hadolint/hadolint
Get-Content frontend/Dockerfile | docker run --rm -i hadolint/hadolint
```

---

## CI/CD Pipeline

The GitHub Actions pipeline runs automatically on every push and pull request to `main`. A failure in any stage stops all subsequent stages.

| Stage | What it does |
|-------|-------------|
| Lint | Runs flake8, ESLint, and hadolint |
| Test | Runs pytest with coverage report |
| Build | Builds and pushes all images to a local registry |
| Security Scan | Scans all images with Trivy, fails on CRITICAL findings |
| Integration Test | Brings the full stack up, submits a job, asserts completion |
| Deploy | Rolling update via SSH — skipped if no deploy target is configured |


## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `REDIS_HOST` | Redis service hostname | `redis` |
| `REDIS_PORT` | Redis service port | `6379` |
| `REDIS_PASSWORD` | Redis authentication password | `` (empty) |
| `API_URL` | API service URL used by the frontend | `http://api:8000` |

---

## Bug Fixes

All bugs found in the original source code are documented in [FIXES.md](./FIXES.md).


