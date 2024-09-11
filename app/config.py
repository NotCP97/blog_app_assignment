import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
QUEUE = os.getenv("QUEUE", "blog_processing_queue")

