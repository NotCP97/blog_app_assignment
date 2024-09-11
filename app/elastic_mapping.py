blog_index_mapping ={
    "settings": {
        "number_of_shards": 3,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "text": {
                "type": "text"
            },
            "title": {
                "type": "text"
            },
            "user_id": {
                "type": "keyword"
            },
            "created_at": {
                "type": "date"
        }
    }
}}

job_index_mapping ={
    "settings": {
        "number_of_shards": 3,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "created_at": {
                "type": "date"
            },
            "status": {
                "type": "keyword"
            },
            "user_id": {
                "type": "keyword"
            },
            "title": {
                "type": "keyword"
            },
            "error": {
                "type": "text"}
        }
    }
}