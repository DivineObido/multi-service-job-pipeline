# FIXES

## Fix 1
**File:**  api/main.py
**Line:**  9 - 12
**Bug:** Redis host and port were hardcoded to localhost and 6379. Inside Docker, containers communicate by service name over a shared network, not localhost. The API container would fail to connect to Redis entirely.
**Fix:** Changed to read from environment variables with sensible defaults.

## Fix 2
**File**: api/main.py
**Line:** 1
**Bug:** HTTPException was not imported from FastAPI, and was needed for Fix 4.
**Fix:** Updated the import line.

## Fix 3
**File**: api/main.py
**Line**: 27
**Bug**: When a job ID was not found in Redis, the API returned {"error": "not found"} with HTTP 200. Clients cannot distinguish between a success and an error when the status code is always 200.
**Fix**: Replaced the plain dict return with a proper HTTP 404 exception.

## Fix 4
**File**: api/main.py
**Line**: missing entirely
**Bug**: No /health endpoint existed on the API. This is required for the Docker HEALTHCHECK instruction and for docker-compose depends_on health conditions to work.
**Fix**: Added a health check endpoint on line 30

## Fix 5
**File:**  worker/worker.py
**Line:**  10 - 14
**Bug:** Redis host and port were hardcoded to localhost and 6379. Inside Docker, containers communicate by service name over a shared network, not localhost. The API container would fail to connect to Redis entirely.
**Fix:** Changed to read from environment variables with sensible defaults.

## Fix 6
**File**: worker/worker.py
**Line**: 34, 40 and 41
**Bug**: The worker ran an infinite while True loop with no way to handle a SIGTERM signal. When Docker stops a container during a rolling update it sends SIGTERM first. Without a handler the worker gets killed immediately mid-job with no cleanup.
**Fix**: Added proper signal handlers and replaced while True with while not shutdown.


## Fix 7
**File**: frontend/app.js
**Line**: 12
**Bug**: API_URL was hardcoded to http://localhost:8000. Inside Docker the frontend container cannot reach the API container via localhost.
**Fix**: Changed to read from an environment variable (added .env file) with a Docker-friendly fallback. Added dotenv for local development. 

## Fix 8
**File**: frontend/app.js
**Line**: 22 - 24 and 33 - 35
**Bug**: Both catch blocks swallowed the actual error and always returned a generic 500. The real error status and message from the API was lost completely.
**Fix**: Forward the actual error status and response body from the API.

## Fix 9
**File**: frontend/app.js
**Line**:  missing entirely
**Bug**: No /health endpoint on the frontend service. Required for Docker HEALTHCHECK and compose dependency checks.
**Fix**: Added a health endpoint before app.listen on line 39

## Fix 10
**File**: frontend/app.js
**Line**: runtime behaviour
**Bug**: Repeated job polling caused axios HTTP socket listeners to accumulate without being cleaned up, triggering a MaxListenersExceededWarning. In production with many concurrent jobs this becomes a real memory leak.
**Fix**: Increased the default max listeners limit at the top of the file.