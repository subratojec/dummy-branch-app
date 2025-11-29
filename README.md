# Branch Loan API — Microloans REST API

A simple, containerized microloans REST API with full multi-environment support (development, staging, production), built with Flask, PostgreSQL, Docker Compose, and GitHub Actions CI/CD.

---

# 1. Running the Application Locally

## Prerequisites

* Docker
* Docker Compose
* Git

---

## Step 1 — Clone the Repository

```bash
git clone https://github.com/<your-username>/dummy-branch-app.git
cd dummy-branch-app
```

---

## Step 2 — Choose the Environment

| Environment | File Loaded    |
| ----------- | -------------- |
| Development | `.env.dev`     |
| Staging     | `.env.staging` |
| Production  | `.env.prod`    |

---

## Step 3 — Start the Application

### Development

```bash
ENV=dev docker compose --profile dev up --build
```

### Staging

```bash
ENV=staging docker compose --profile staging up --build
```

### Production

```bash
ENV=prod docker compose --profile prod up --build
```

---

## Step 4 — Test API Endpoints

| Endpoint         | Description          |
| ---------------- | -------------------- |
| `GET /health`    | Check service health |
| `GET /api/loans` | List all loans       |
| `GET /api/stats` | Summary statistics   |

### Example (Staging)

```bash
curl http://localhost:8001/health
```

---

# 2. Switching Between Environments

Docker Compose automatically loads the environment file based on the `ENV` variable.

### Examples:

```bash
# Development
ENV=dev docker compose --profile dev up

# Staging
ENV=staging docker compose --profile staging up

# Production
ENV=prod docker compose --profile prod up
```

---

# 3. Environment Variables Explained

## Development — `.env.dev`

| Variable                   | Meaning                 |
| -------------------------- | ----------------------- |
| ENV=dev                    | Development mode        |
| FLASK_ENV=development      | Auto reload, debug mode |
| LOG_LEVEL=debug            | Verbose logs            |
| POSTGRES_USER=postgres     | Local DB user           |
| POSTGRES_PASSWORD=postgres | Local DB password       |
| POSTGRES_DB=microloans     | Development DB          |
| API_PORT=8000              | API port                |
| DB_PORT=5432               | Local DB port           |

---

## Staging — `.env.staging`

| Variable                  | Meaning                        |
| ------------------------- | ------------------------------ |
| POSTGRES_USER=stguser     | Staging DB user                |
| POSTGRES_PASSWORD=stgpass | Staging DB pass                |
| POSTGRES_DB=loans_staging | Staging DB                     |
| DB_PORT=5433              | Exposed DB port                |
| DB_INTERNAL_PORT=5432     | Internal Postgres port         |
| FLASK_ENV=production      | Production behavior            |
| LOG_LEVEL=info            | Cleaner logs                   |
| API_PORT=8001             | Staging API port               |
| DEV_MOUNT=false           | Disables dev hot-reload mounts |
| DATABASE_URL              | Full DB connection string      |

---

## Production — `.env.prod`

| Variable                             | Meaning             |
| ------------------------------------ | ------------------- |
| ENV=prod                             | Production mode     |
| FLASK_ENV=production                 | Production settings |
| LOG_LEVEL=error                      | Minimal logs        |
| POSTGRES_DB=loans                    | Production DB name  |
| POSTGRES_USER=produser               | Prod DB user        |
| POSTGRES_PASSWORD=verysecurepassword | Prod DB password    |
| API_PORT=8000                        | Production API port |
| DB_PORT=5432                         | Production DB port  |

---

# 4. CI/CD Pipeline (GitHub Actions)

Pipeline triggers:

* push to main
* pull_request → build + scan only

## Pipeline Stages

### 1. Test Stage

* Install dependencies
* Run tests (pytest)
* Fail early if tests fail

### 2. Build Stage

* Build Docker image
* Tag with commit SHA
* Upload TAR artifact for debugging

### 3. Security Scan Stage

* Scan with Trivy
* Fail on HIGH or CRITICAL vulnerabilities

### 4. Push Stage (main only)

Repository: GitHub Container Registry

```
ghcr.io/<owner>/dummy-branch-app:<commit-sha>
ghcr.io/<owner>/dummy-branch-app:latest
```

---

# 5. Architecture Diagram

```
              +-------------------+
              |   Host Machine    |
              +-------------------+
                       |
                       |
              +-------------------+
              |  Docker Compose   |
              +-------------------+
                       |
   ------------------------------------------------
   |                      |                       |
+---------+        +--------------+        +----------------+
|  API    | <----> |   Postgres   |        |     Nginx      |
| Flask   |        |   Database   | <----> | Reverse Proxy  |
+---------+        +--------------+        +----------------+
   |                       |
   |                       |
 REST API          Loan / Stats Data
```

---

# 6. Design Decisions

| Decision                 | Reason                                 |
| ------------------------ | -------------------------------------- |
| Single Compose File      | Consistency across environments        |
| Env Files                | Simple control over environment config |
| Volume Mounts (dev only) | Enable hot-reload                      |
| Gunicorn                 | Production-ready WSGI server           |
| Nginx                    | Optional reverse proxy with SSL        |
| GHCR Registry            | Private + versioned image storage      |

---

# 7. Trade-offs Considered

| Decision            | Trade-off                        |
| ------------------- | -------------------------------- |
| Single Compose File | More complex interpolation logic |
| Containerized DB    | Slower than native DB            |
| Gunicorn            | More config complexity           |
| Using GHCR          | Requires authentication setup    |

---

# 8. Future Improvements

* [ ] Add deployment stages (VM / Kubernetes / ECS)
* [ ] Automated Alembic migrations
* [ ] Integration tests & load testing (Locust)
* [ ] Monitoring & metrics (Prometheus/Grafana)
* [ ] Use secret manager (Vault/AWS Secrets Manager)

---

# 9. Troubleshooting

### API shows database errors

```bash
docker compose logs api
```

Check `DATABASE_URL` / DB credentials.

---

### Nginx SSL errors

```bash
ls docker/nginx/cert.pem
ls docker/nginx/key.pem
```

Fix permissions:

```bash
chmod 644 docker/nginx/key.pem
```

---

### Reset the database

```bash
docker compose down -v
docker compose up --build
```

---

# 10. Health Checks

### API

```bash
curl http://localhost:<API_PORT>/health
```

### Database

```bash
docker compose exec db psql -U <user> -d <db>
```

### Containers Status

```bash
docker compose ps
```
