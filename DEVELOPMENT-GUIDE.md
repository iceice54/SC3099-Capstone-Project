# SAIV Developer Setup & Quickstart Guide

This guide provides practical instructions for setting up the local environment, running the services, executing tests, and collaborating across the 4 modules.

---

## 1. Dependency Management (`requirements.txt`)

You do **NOT** need to manually install each individual module's `requirements.txt` on your machine:

| Dependency File | Target | Purpose |
|---|---|---|
| **`requirements-test.txt`** (root) | **Local Python `.venv`** | **Master file combining Modules 2, 3, 4 + Pytest**. Installing this once gives your IDE complete code completion and allows running `pytest`. |
| **`moduleX/requirements.txt`** | **Docker Containers** | Used automatically by Docker when building each microservice image to keep container sizes minimal. |
| **`module1-frontend/package.json`** | **Node.js Environment** | Next.js frontend dependencies (install via `npm install` inside `module1-frontend`). |

---

## 2. Setting Up Your Local Environment

In the root directory of the project:

```bash
# 1. Create a Python virtual environment
python3 -m venv .venv

# 2. Activate the virtual environment
source .venv/bin/activate       # On Linux / macOS
# On Windows PowerShell: .venv\Scripts\Activate.ps1
# On Windows CMD:        .venv\Scripts\activate.bat

# 3. Upgrade pip and install all unified dependencies
pip install --upgrade pip
pip install -r requirements-test.txt
```

---

## 3. Development Workflows

### Option A: Hybrid Development (Recommended for Fast Iteration)
Databases run in Docker, while your microservices run locally on your host machine with **live hot-reload** enabled (no waiting for container rebuilds).

1. **Start database & infrastructure containers:**
   ```bash
   docker compose up -d postgres redis prometheus grafana
   docker compose ps
   ```

2. **Run Module 2 (Backend API) locally:**
   ```bash
   cd module2-backend
   export DATABASE_URL="postgresql://saiv:saiv_password@localhost:5434/saiv"
   export REDIS_URL="redis://localhost:6380/0"
   export SECRET_KEY="dev-secret-key-change-in-prod"
   export FACE_SERVICE_URL="http://localhost:8001"

   uvicorn app.main:app --reload --port 8000
   ```

3. **Run Module 3 (Face Recognition & Risk) locally:**
   ```bash
   cd module3-face-recognition
   export REDIS_URL="redis://localhost:6380/0"

   uvicorn app.main:app --reload --port 8001
   ```

4. **Run Module 1 (Frontend PWA) locally:**
   ```bash
   cd module1-frontend
   npm install
   npm run dev
   ```

5. **Run Module 4 (Instructor Dashboard) locally:**
   ```bash
   cd module4-observability
   export DATABASE_URL="postgresql://saiv:saiv_password@localhost:5434/saiv"
   export BACKEND_URL="http://localhost:8000"
   export PROMETHEUS_URL="http://localhost:9090"

   streamlit run app/main.py --server.port 8501
   ```

---

### Option B: Full Docker Compose (Integration / Staging Mode)
Run all 4 application modules and all infrastructure containers inside Docker:

```bash
# Build and start all services in background
docker compose up -d --build

# View container logs
docker compose logs -f

# Check container health status
docker compose ps
```

---

## 4. Service URLs & Port Reference

| Service | Port (Host) | URL | Notes |
|---|---|---|---|
| **Module 1 (Frontend)** | `3000` | http://localhost:3000 | Next.js Student PWA |
| **Module 2 (Backend API)** | `8000` | http://localhost:8000/docs | Swagger UI API docs |
| **Module 3 (Face Recognition)** | `8001` | http://localhost:8001/docs | FastAPI docs & CV endpoints |
| **Module 4 (Dashboard)** | `8501` | http://localhost:8501 | Streamlit Instructor Dashboard |
| **PostgreSQL Database** | `5434` | `localhost:5434` (db: `saiv`, user: `saiv`, pass: `saiv_password`) | Mapped to 5432 internally |
| **Redis Cache / Rate Limit**| `6380` | `localhost:6380` | Mapped to 6379 internally |
| **Prometheus Metrics** | `9090` | http://localhost:9090 | Metrics collector |
| **Grafana Dashboards** | `3001` | http://localhost:3001 | `admin` / `admin` |

---

## 5. Running the Automated Test Suite

> **Note:** Tests send HTTP requests to running services. Ensure your backend (`:8000`) and face recognition service (`:8001`) are up before testing.

From the project root:

```bash
# Activate virtual environment
source .venv/bin/activate

# Set test target URLs (defaults to localhost)
export TEST_BACKEND_URL="http://localhost:8000"
export TEST_FACE_URL="http://localhost:8001"

# Run all public tests (90 points)
pytest tests/public/ -v

# Run module-specific tests:
pytest tests/public/test_face_recognition.py -v     # Module 3 (15 pts)
pytest tests/public/test_api_functional.py -v       # Module 2 (26 pts)
pytest tests/public/test_security_basic.py -v       # Security & RBAC (12 pts)
pytest tests/public/test_privacy_basic.py -v        # Privacy & Retention (8 pts)
pytest tests/public/test_frontend_dashboard.py -v   # Contract tests (8 pts)
pytest tests/public/test_observability.py -v        # Observability & Stats (12 pts)
pytest tests/public/test_performance.py -v          # Performance & Latency (5 pts)
pytest tests/public/test_integration.py -v          # End-to-End Flow (4 pts)
```

---

## 6. Stopping & Resetting Infrastructure

```bash
# Stop all Docker services
docker compose down

# Stop and wipe database volumes (clean slate)
docker compose down -v
```

---

## 7. Project Timeline & Milestones

For the complete week-by-week 10-week implementation timeline and task breakdown for all 4 modules, see:
👉 **[TIMELINE.md](TIMELINE.md)**

