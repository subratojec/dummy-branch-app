FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# ---- SECURITY: upgrade OS packages to reduce CVEs ----
RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
      netcat-traditional \
      ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# ---- Install dependencies ----
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt

# ---- Copy source code ----
COPY . .

# ---- Create non-root user ----
RUN useradd --create-home appuser \
 && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "wsgi:app"]
