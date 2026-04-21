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
COPY worker.py .

# Switch to non-root user
USER appuser


HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import redis, os; r = redis.Redis(host=os.getenv('REDIS_HOST', 'redis'), port=int(os.getenv('REDIS_PORT', 6379)), password=os.getenv('REDIS_PASSWORD', None)); r.ping()"


CMD [ "python", "worker.py" ]