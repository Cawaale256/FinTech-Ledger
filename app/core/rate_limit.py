import time
from collections import defaultdict

# Simple in-memory store (swap with Redis later)
request_log = defaultdict(list)

MAX_REQUESTS = 10          # allowed requests
WINDOW_SECONDS = 60        # per 60 seconds
