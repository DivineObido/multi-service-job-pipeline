# Builder stage
FROM node:lts-alpine3.22 AS builder

WORKDIR /app

# Copy packages file
COPY packages*.json ./
RUN npm ci --only=production

# Final stage
FROM node:lts-alpine3.22 

WORKDIR /app

RUN groupadd --system appgroupp && \
    useradd --system --gid appgroup appuser

# Copy installed dependencies from builder
COPY --from=builder /app/node_modules ./node_modules

# Copy application code
COPY app.js .
COPY views/ ./views
COPY package.json .

# Switch to non-rooot user
USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => { process.exit(r.statusCode === 200 ? 0 : 1) })"

CMD [ "node", "app.jjs" ]