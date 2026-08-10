# ═══════════════════════════════════════════════════════════════════
# CP2 — Containerization (Production‑ready)
#
# Multi‑stage build, slim base, non‑root user, HEALTHCHECK, PORT from env.
# ═════════════════════════════════════════════════════════════════==

# ---------- Stage 1: Builder ----------
FROM python:3.11-slim AS builder
WORKDIR /app

# Install build dependencies (only needed for pip install)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (cached layer)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY . .

# ---------- Stage 2: Runtime ----------
FROM python:3.11-slim AS runtime
WORKDIR /app

# Create a non‑root user
RUN groupadd -r appgroup && useradd -r -g appgroup -s /bin/bash appuser

# Copy only the installed packages and application code from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app /app

# Ensure non‑root ownership
RUN chown -R appuser:appgroup /app

# Switch to the non‑root user
USER appuser

# Expose the service port (default 8000, can be overridden by PORT env var)
EXPOSE 8000

# Healthcheck – calls the /health endpoint
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Entry point – use uvicorn (the app reads PORT from settings)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
