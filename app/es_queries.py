def search_blogs_query(query: str = None, user_id: str = None):
    body = {
        "query": {
            "bool": {}
        },
        "sort": {
            "created_at": {"order": "desc"}
        },
        "_source": ["title", "text", "user_id", "created_at"]
    }
    if query:
        body["query"]["bool"] = {
            "should": [
                {
                    "match": {
                        "blog_title": {
                            "query": query,
                            "boost": 3.0
                        }
                    }
                },
                {
                    "match": {
                        "blog_text": {
                            "query": query,
                            "fuzziness": "AUTO"
                        }
                    }
                }
            ]
        }
    if user_id:
        body["query"]["bool"] = {
            "filter": {
                "term": {
                    "user_id": user_id
                }
            }
        }
    return body

def user_blogs_query(user_id: str):
    return {
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


def user_submitted_blogs_query(user_id: str):
    return {
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
        "_source": ["title", "user_id", "created_at", "status", "error"]
    }

