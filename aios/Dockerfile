# ANTIGRAVITY OMEGA AIOS: Zero-Dependency Autonomous Micro-OS
# Multi-stage lightweight Python 3.12-slim base
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    AIOS_PORT=8090 \
    DATA_DIR=/app/data

WORKDIR /app

# Create non-root system user for security
RUN groupadd -g 1001 aios && \
    useradd -u 1001 -g aios -m -s /bin/bash aios && \
    mkdir -p /app/data /app/dashboards /app/logs && \
    chown -R aios:aios /app

COPY --chown=aios:aios ai/ /app/ai/
COPY --chown=aios:aios automation/ /app/automation/
COPY --chown=aios:aios databases/ /app/databases/
COPY --chown=aios:aios projects/ /app/projects/
COPY --chown=aios:aios scripts/ /app/scripts/
COPY --chown=aios:aios dashboards/ /app/dashboards/

USER aios

EXPOSE 8090 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request, sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8090/health').status == 200 else 1)"

CMD ["python", "ai/gateway.py"]
