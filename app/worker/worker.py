import os

from redis import Redis
from rq import Queue, SimpleWorker

redis_host = os.getenv("REDIS_HOST","localhost")

redis_conn = Redis(host=redis_host, port=6379, db=0)

queue = Queue( "document_processing", connection=redis_conn )

worker = SimpleWorker( [queue], connection=redis_conn )

worker.work()