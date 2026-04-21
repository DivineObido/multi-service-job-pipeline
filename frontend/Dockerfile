# Builder stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy packages file
COPY package*.json ./
RUN npm ci --omit=dev

# Final stage
FROM node:20-alpine

WORKDIR /app

RUN addgroup -S appgroup && \
    adduser -S -G appgroup appuser

# Copy installed dependencies from builder
COPY --from=builder /app/node_modules ./node_modules

# Copy application code
COPY app.js .
COPY views/ ./views
COPY package.json .

# Switch to non-root user
USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => { process.exit(r.statusCode === 200 ? 0 : 1) })"

CMD [ "node", "app.js" ]