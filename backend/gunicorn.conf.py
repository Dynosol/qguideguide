import multiprocessing
import os

# Number of worker processes
workers = 2  # Reduced from default to conserve memory
threads = 1  # Single thread per worker for thread safety

# Worker settings
worker_class = 'sync'  # Use sync workers instead of gevent
worker_connections = 1000

# Timeouts
timeout = 120  # Increased timeout for large data loads
graceful_timeout = 30
keepalive = 5

# Memory management
max_requests = 1000  # Restart workers after handling this many requests
max_requests_jitter = 50  # Add randomness to the restart interval
worker_tmp_dir = "/dev/shm"  # Use RAM for temp files

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Process naming
proc_name = 'qguideguide_api'

# SSL config (if needed)
keyfile = None
certfile = None

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Server socket
bind = "0.0.0.0:10000"
backlog = 2048

def post_fork(server, worker):
    """
    Called just after a worker has been forked.
    """
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def pre_fork(server, worker):
    """
    Called just prior to forking a worker.
    """
    pass

def pre_exec(server):
    """
    Called just prior to forking a new master.
    """
    server.log.info("Forked master process: %d", os.getpid())
