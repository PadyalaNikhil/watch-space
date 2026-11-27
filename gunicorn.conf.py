"""
Gunicorn configuration for production deployment (Render, Railway, VPS, Fly.io).
Supports large video and file uploads (up to 10 GB) with zero body-size limits.
"""
import os

bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"
workers = int(os.environ.get('WEB_CONCURRENCY', '2'))
threads = 4
timeout = 300
keepalive = 65

# 0 disables gunicorn's HTTP request body ceiling so 10 GB video uploads stream cleanly
limit_request_body = 0
limit_request_line = 8190
limit_request_fields = 200
accesslog = '-'
errorlog = '-'
loglevel = 'info'
