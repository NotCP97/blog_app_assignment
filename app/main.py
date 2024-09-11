from fastapi import FastAPI, HTTPException
from model import BlogPost
import time
from rq import Queue
from consumer import process_blog_post
from clients import RedisHandler, ElasticsearchHandler
from app_scripts import lifespan
import uuid
from loggerz import get_logger


logger = get_logger()

app = FastAPI(lifespan=lifespan)

es_handler = ElasticsearchHandler()
redis_handler = RedisHandler()

@app.get("/health_check")
def health_check():
    return {"status": "ping pong"}

 

@app.post("/blogs/submit")
async def submit_blog(blog: BlogPost):
    """
    This endpoint will submit the blog post to the queue for processing
    """
    if blog.user_id not in {"user1", "user2", "user3", "user4", "user5"}:
        raise HTTPException(status_code=401, detail="Invalid user")
    
    job_id = str(uuid.uuid4())

    blog_data = blog.model_dump()
    blog_data["created_at"] = int(time.time()*1000)
    blog_data["job_id"] = job_id

    # we should index this blog job id to elasticsearch with status as submitted for the user to check the status of the job before sending it to the queue
    
    job = redis_handler.add_job(process_blog_post, blog_data, job_id=job_id)
    return {"message": "Blog post submitted successfully", "job_id": job.id}

@app.get("/blogs/search")
def search_blogs(query: str,user_id: str = None, from_: int = 0, size: int = 10):
    """
    This endpoint will search the blogs in elasticsearch
    """
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "text"]
            }
        },
        "sort": {
            "created_at": {"order": "desc"}
        },
        "_source": ["title", "text", "user_id", "created_at"]
    }
    if user_id:
        body["query"]["bool"] = {
            "filter": {
                "term": {
                    "user_id": user_id
                }
            }
        }

    results = es_handler.get_results(index="blogs", body=body, from_=from_, size=size)
    return {"data": [result["_source"] for result in results["hits"]["hits"]], "total_hits": results["hits"]["total"]["value"]}
    
@app.get("/blogs/user_blogs")
def user_blogs(user_id: str, from_: int = 0, size: int = 10):
    body = {
        "query": {
            "bool": {
                "filter": {
                "term": {
                    "user_id": user_id
                }
            }
            }
        },

        "sort": {
            "created_at": {"order": "desc"}
        },
        "_source": ["title", "text", "user_id", "created_at"]
    }
    results = es_handler.get_results(index="blogs", body=body, from_=from_, size=size)
    return {"data": [result["_source"] for result in results["hits"]["hits"]], "total_hits": results["hits"]["total"]["value"]}

@app.get("/blogs/user_submitted_blogs")
def user_submitted_blogs(user_id: str, from_: int = 0, size: int = 10):
    body = {
        "query": {
            "bool": {
                "filter": {
                "term": {
                    "user_id": user_id
                }
            }
            }
        },
        "sort": {
            "created_at": {"order": "desc"}
        }
    }
    results = es_handler.get_results(index="submitted_jobs", body=body, from_=from_, size=size)
    return {"data": [result["_source"] for result in results["hits"]["hits"]], "total_hits": results["hits"]["total"]["value"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)