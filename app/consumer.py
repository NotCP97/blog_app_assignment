from clients import ElasticsearchHandler, RedisHandler

from rq import Worker, Queue, Connection
from hashlib import md5
from loggerz import get_logger
import time

logger = get_logger()


es_handler = ElasticsearchHandler()


def process_blog_post(blog_post) -> str:
    """
    This function will process the blog post

    :param blog_post: Blog post
    :type blog_post: dict
    :return: Processed blog post
    :rtype: str
    
    """
    logger.info(f"Processing blog post: {blog_post['title']}")
    # checking if new blog is not duplicate

    blog_hash = md5((blog_post["text"]+blog_post["title"]).encode()).hexdigest()  # we can add user_id to the hash to make it unique for the user

    job_submitted_doc = {
        "status": "processing",
        "error": "",
        "text": blog_post["text"],
    }

    if es_handler.get_result_by_id(index="blogs", id=blog_hash):
        job_submitted_doc["status"] = "failed"
        job_submitted_doc["error"] = f"Blog post already exists: {blog_post['title']}"
        _ = es_handler.update_doc_by_id(index="submitted_jobs", body={"doc":job_submitted_doc}, doc_id=blog_post["job_id"])
        return f"Blog post already exists: {blog_post['title']}"
    
    # Index the blog post
    _ = es_handler.index_doc(index="blogs", body=blog_post, doc_id=blog_hash)
    job_submitted_doc["status"] = "success"
    # Index the job submitted doc
    _ = es_handler.update_doc_by_id(index="submitted_jobs", body={"doc":job_submitted_doc}, doc_id=blog_post["job_id"])


    return f"Processed blog post: {blog_post['title']}"



# Connect to Redis
redis_conn = RedisHandler().get_client()


if __name__ == '__main__':
    try:
        with Connection(redis_conn):
            worker = Worker(list(map(Queue, ['blog_processing_queue'])))
            worker.work()
    except Exception as e:
        logger.error(f"Error: {e}")
        time.sleep(10)
        raise e
