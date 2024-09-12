from contextlib import asynccontextmanager
from fastapi import FastAPI
from clients import ElasticsearchHandler
from elastic_mapping import blog_index_mapping, job_index_mapping
from elasticsearch import exceptions
import time, sys
from loggerz import get_logger


logger = get_logger()

def start_up():
    es_handler = ElasticsearchHandler()

    retries = 100  # Number of retries before exiting
    for i in range(retries):
        try:
            if es_handler.es.ping():
                logger.info("Successfully connected to Elasticsearch")
                if not es_handler.es.indices.exists(index="blogs"):
                    es_handler.es.indices.create(index="blogs", body=blog_index_mapping)
                    logger.info("Created index 'blogs'")

                if not es_handler.es.indices.exists(index="submitted_jobs"):
                    es_handler.es.indices.create(index="submitted_jobs", body=job_index_mapping)
                    logger.info("Created index 'submitted_jobs'")
                break
            else:
                logger.info(f"Attempt {i + 1}/{retries} failed to connect to Elasticsearch. Retrying in 10 seconds...")
                time.sleep(10)
        except exceptions.ConnectionError:
            logger.info(f"Attempt {i + 1}/{retries} failed to connect to Elasticsearch. Retrying in 10 seconds...")
            time.sleep(10)

    if es_handler.es.ping():
        logger.info("Successfully connected to Elasticsearch")

    else:
        logger.error("Failed to connect to Elasticsearch. Exiting...")
        sys.exit(1)

    logger.info("Starting up...")

def shut_down():
    logger.info("Shutting down...")

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_up()
    yield
    shut_down()