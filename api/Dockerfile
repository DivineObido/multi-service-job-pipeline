# Build Stage
FROM python:3.11-alpine3.22 AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install upgrade && pip install update \
    pip install --no-cache-dr --prefix=/install -r requirements.txt

# Final Stage
FROM python:3.11-alphine

WORKDIR /app

# Create non-root user
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

# Copy installed dependencies from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY main.py .

# Switch to non-root user
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"


CMD [ "uvicorn". "main:app", "--host", "0.0.0.0", "--port", "8000" ]