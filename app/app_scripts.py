from contextlib import asynccontextmanager
from fastapi import FastAPI
from clients import ElasticsearchHandler
from elastic_mapping import blog_index_mapping, job_index_mapping
from elasticsearch import exceptions
import time

def start_up():
    es_handler = ElasticsearchHandler()

    retries = 5  # Number of retries before exiting
    for i in range(retries):
        try:
            if es_handler.es.ping():
                print("Successfully connected to Elasticsearch")
                if not es_handler.es.indices.exists(index="blogs"):
                    es_handler.es.indices.create(index="blogs", body=blog_index_mapping)
                    print("Created index 'blogs'")

                if not es_handler.es.indices.exists(index="submitted_jobs"):
                    es_handler.es.indices.create(index="submitted_jobs", body=job_index_mapping)
                    print("Created index 'submitted_jobs'")
                break
            else:
                print(f"Attempt {i + 1}/{retries} failed to connect to Elasticsearch. Retrying in 5 seconds...")
                time.sleep(5)
        except exceptions.ConnectionError:
            print(f"Attempt {i + 1}/{retries} failed to connect to Elasticsearch. Retrying in 5 seconds...")
            time.sleep(5)

    es_handler.es.close()

    print("Starting up...")

def shut_down():
    print("Shutting down...")

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_up()
    yield
    shut_down()