import os
from redis import Redis
from rq import Queue

redis_host = os.getenv("REDIS_HOST", "localhost")

redis_conn = Redis(host=redis_host, port=6379, db=0)

document_queue = Queue("document_processing", connection=redis_conn)