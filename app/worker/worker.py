from redis import Redis
from rq import Queue, SimpleWorker

redis_conn = Redis(host="localhost", port=6379, db=0)

queue = Queue( "document_processing", connection=redis_conn )

worker = SimpleWorker( [queue], connection=redis_conn )

worker.work()