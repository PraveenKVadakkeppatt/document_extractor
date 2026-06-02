from redis import Redis
from rq import Queue

redis_conn = Redis(host="redis", port=6379, db=0)

document_queue = Queue("document_processing", connection=redis_conn)