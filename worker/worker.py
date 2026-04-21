from dotenv import load_dotenv
import redis
import time
import os
import sys
import signal

load_dotenv()

r = redis.Redis(
    # host="localhost",
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD", None)
    )


shutdown = False


def handle_shutdown(signum, frame):
    global shutdown
    print("Shutdown signal received, finishing current job...")
    shutdown = True


signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)


def process_job(job_id):
    print(f"Processing job {job_id}")
    time.sleep(2)  # simulate work
    r.hset(f"job:{job_id}", "status", "completed")
    print(f"Done: {job_id}")


while not shutdown:
    job = r.brpop("job", timeout=5)
    if job:
        _, job_id = job
        process_job(job_id.decode())

print("Worker shut down cleanly.")
sys.exit(0)
