from fastapi import FastAPI, HTTPException
from model import BlogPost
import time
from consumer import process_blog_post
from clients import RedisHandler, ElasticsearchHandler
from app_scripts import lifespan
import uuid
from loggerz import get_logger

from es_queries import search_blogs_query, user_blogs_query, user_submitted_blogs_query


logger = get_logger()

app = FastAPI(lifespan=lifespan, docs_url="/api/docs", redoc_url="/api/redoc")

es_handler = ElasticsearchHandler()
redis_handler = RedisHandler()



@app.get("/health_check")
def health_check():
    """
    This endpoint will return the status of the service
    """
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

    submit_blog_doc = {
        "status": "submitted",
        "user_id": blog.user_id,
        "title": blog.title,
        "created_at": blog_data["created_at"]
    }

    _ = es_handler.index_doc(index="submitted_jobs", body=submit_blog_doc, doc_id=job_id)
    
    job = redis_handler.add_job(process_blog_post, blog_data, job_id=job_id)
    return {"message": "Blog post submitted successfully", "job_id": job.id}

@app.get("/blogs/status/{job_id}")
def get_blog_status(job_id: str):
    """
    This endpoint will return the status of the blog post
    """
    data =  es_handler.get_result_by_id(index="submitted_jobs", id=job_id)
    if not data:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"data": data}

@app.get("/blogs/search")
def search_blogs(query: str = None,user_id: str = None, from_: int = 0, size: int = 10):
    """
    This endpoint will search the blogs in elasticsearch
    """
    
    body = search_blogs_query(query=query, user_id=user_id)
    
    return es_handler.get_results_with_pagination(index="blogs", body=body, from_=from_, size=size)
    
@app.get("/blogs/user_blogs/{user_id}")
def user_blogs(user_id: str, from_: int = 0, size: int = 10):
    
    body = user_blogs_query(user_id=user_id)
    
    return es_handler.get_results_with_pagination(index="blogs", body=body, from_=from_, size=size)

@app.get("/blogs/user_submitted_blogs/{user_id}")
def user_submitted_blogs(user_id: str, from_: int = 0, size: int = 10):
    
    body = user_submitted_blogs_query(user_id=user_id)
    
    return es_handler.get_results_with_pagination(index="submitted_jobs", body=body, from_=from_, size=size)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)