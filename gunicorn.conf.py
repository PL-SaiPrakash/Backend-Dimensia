# Gunicorn configuration file for production
import multiprocessing

# The socket to bind
bind = "0.0.0.0:$PORT"  # Render will provide the PORT environment variable

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'

# Logging
accesslog = '-'
errorlog = '-'

# Timeout settings
timeout = 120  # 3D model processing may take time

# Reload in development
reload = False