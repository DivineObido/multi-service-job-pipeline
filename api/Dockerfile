# Build Stage
FROM python:3.11-alpine AS builder

WORKDIR /app

COPY requirements.txt .
# hadolint ignore=DL3013
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

    # Final Stage
FROM python:3.11-alpine

WORKDIR /app

# Create non-root user
RUN addgroup -S appgroup && \
    adduser -S -G appgroup appuser

# Copy installed dependencies from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY main.py .

# Switch to non-root user
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]