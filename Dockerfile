# Multi-stage production container for Planetary Sovereign Continuum & Frontier Engine
FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PORT=8000

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
RUN pip install --no-cache-dir \
    fastapi==0.141.1 \
    uvicorn[standard]==0.34.0 \
    pydantic==2.10.6 \
    httpx==0.28.1 \
    pytest==9.1.1

# Create non-root user
RUN addgroup --system sovereign && adduser --system --group sovereign

# Copy application modules
COPY terra_kinetics/ /app/terra_kinetics/
COPY aether_energy/ /app/aether_energy/
COPY bioma_foundry/ /app/bioma_foundry/
COPY sovereign_continuum/ /app/sovereign_continuum/
COPY .agent/ /app/.agent/
COPY AGENTS.md /app/AGENTS.md

# Set ownership
RUN chown -R sovereign:sovereign /app

USER sovereign

EXPOSE 8000 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "sovereign_continuum.api.gateway:app", "--host", "0.0.0.0", "--port", "8000"]
