from app.queue import document_queue


job = document_queue.enqueue(print, "Hello RQ")

print(job.id)