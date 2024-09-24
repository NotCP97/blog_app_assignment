# Blogging Service

Hi readers,

Creating this repository as part of ***** recruitment assignment.

Assumption  - We dont have separate redis and elastic search db


Currently service supports for limited user_ids
 - user1, user2, user3, user4, user5 (Can be improved with sign-up and login functionality)

This repository contains a simple, scalable blogging service designed to allow users to submit and search blog entries. The service includes the following core components:

1. **Blog Submission API** (FastAPI-based)
2. **Queue Consumer** (Redis-based using `rq` for asynchronous processing)
3. **Elasticsearch Database** for storing blog entries
4. **Search API** for querying blog titles and text

All components are containerized using Docker, and the project includes deployment scripts for both Docker Compose and Kubernetes.

## Table of Contents

- [Architecture](#architecture)
- [Components](#components)
- [Setup](#setup)
- [APIs](#apis)
- [Testing](#testing)
- [Improvements](#improvements)
- [Deployment](#deployment)

# Architecture

The service follows a microservices-like architecture where:

1. **Blog entries** are submitted asynchronously through a FastAPI-based REST API.
2. **Queue Consumer** processes the blog submissions from a Redis queue and writes them to an Elasticsearch database.
3. **Search API** allows users to search through stored blog entries using Elasticsearch's full-text search capabilities.

![screenshot](architecture.png)


# Components

The project includes the following:

1. **FastAPI Backend** (`/app/main.py`)
   - Blog submission and search APIs
   - User specific api to track user submissions and submissions progress
   - Dockerized with a lightweight Python image

2. **Redis Queue Consumer** (`/app/consumer.py`)
   - Processes submissions from Redis and stores them in Elasticsearch.

3. **Elasticsearch**
   - Stores the blog entries.
   - Stores users submission history and submission status

4. **Docker Compose** (`docker-compose.yml`)
   - Orchestrates all components (FastAPI, Redis, Elasticsearch, Queue Consumer).

5. **Kubernetes Deployment Files** (`/k8s`)
   - Kubernetes manifests for deployment of FastAPI, Redis, and Elasticsearch.

# Setup

### Prerequisites

- Docker & Docker Compose
- Kubernetes (if deploying on K8s)
- `curl` for API testing

### Local Development (Docker Compose)

1. Clone the repository:

```bash
git clone <repo_url>
cd blogging-service/app
```
start docker compose 
```bash
docker-compose up --build
```
This will start:

1. FastAPI service on http://localhost:8000
2. Redis queue on http://localhost:6379
3. Elasticsearch on http://localhost:9200
4. Swagger-UI for FastAPI service on http://localhost:8000/api/docs


# APIs
### Blog Submission API
Endpoint: `POST /blogs/submit`
 

Request:
```json
{
  "blog_title": "My First Blog",
  "blog_text": "This is the content of my blog.",
  "user_id": "user1"
}
```

Response: 
```json
{
  "message": "Blog post submitted successfully",
  "job_id": "6f1f8749-bda0-48f2-a2f9-992a900f2dc7"
}
```

### Search API
Endpoint: `POST /blogs/search?query=<search_term>`


Request:
```bash
GET blogs/search?query=First
```

Response: 
```json

{
  "data": [
    {
      "user_id": "user3",
      "created_at": 1726111438395,
      "text": "njnc",
      "title": "njdnj"
    }
  ],
  "total_hits": 1,
  "start": 0,
  "end":1
}
```


### USERS Blogs and Users Submission status
#### User Blogs

Endpoint: `GET /blogs/user_blogs/<user_id>`


Request:
```bash
GET /blogs/user_blogs/<user_id>
```

Response: 
```json
{
  "data": [
    {
      "user_id": "user3",
      "created_at": 1726111438395,
      "text": "njnc",
      "title": "njdnj"
    }
  ],
  "total_hits": 1,
   "start": 0,
   "end":1
}
```

#### User Submissions
Endpoint: `GET /blogs/user_submitted_blogs/<user_id>`

Request:
```bash
GET /blogs/user_submitted_blogs/<user_id>
```

Response: 
```json
{
  "data": [
    {
      "created_at": 1726114891350,
      "status": "failed",
      "user_id": "user4",
      "title": "bbd hdbhi dhbhd shbh",
      "error": "Blog post already exists: bbd hdbhi dhbhd shbh",
      "text": "This is the content of my blog."
    },
    {
      "created_at": 1726111451172,
      "status": "failed",
      "user_id": "user4",
      "title": "bbd hdbhi dhbhd shbh",
      "error": "Blog post already exists: bbd hdbhi dhbhd shbh",
       "text": "This is the content of my blog."
    },
    {
      "created_at": 1726111451006,
      "status": "success",
      "user_id": "user4",
      "title": "bbd hdbhi dhbhd shbh",
      "error": "",
      "text": "This is the content of my blog."
    }
  ],
   "total_hits": 3
   "start": 0,
   "end":3
}
```

### Submitted job Status

Endpoint : `/blogs/status/<job_id>`

Request:
```bash
GET /blogs/status/<job_id>
```

Response: 
```json
{
  "data": {
    "created_at": 1726170123780,
    "status": "failed",
    "user_id": "user4",
    "title": "bbd hdbhi dhbhd shbh",
    "error": "Blog post already exists: bbd hdbhi dhbhd shbh",
    "text": "This is the content of my blog."
  }
}
```


### Health_check


Endpoint: `GET /health_check'


Request:
```bash
GET /health_check
```

Response: 
```json

{
  "status": "ping pong"
}
```


# Testing

You can test the APIs using `curl` commands:

### Blog Submission

```bash
curl -X POST "http://localhost:8000/blogs/submit" \
-H "Content-Type: application/json" \
-d '{
  "blog_title": "Test Blog",
  "blog_text": "This is a test blog post.",
  "user_id": "user1"
}'
```

### Search Blog
```bash
curl "http://localhost:8000/search?query=Test"
```

### Elasticsearch Mapping

```bash
curl -X GET "http://localhost:9200/blogs/_mapping"
```

# Improvements

- **User Authentication**: Add authentication to secure the blog submission and search API.
- **Content Rich Blogs**: Currently System only support text content in the blog but we should add images, gifs and videos to blogs
- **Notification Service**: Notify user blog proceesing status
- **Rate Limiting**: Implement rate limiting to prevent abuse of the submission API.
- **Full-Text Search Enhancements**: Improve search with more complex queries such as fuzzy matching or boosting blog titles in results.
- **Monitoring & Logging**: Integrate services like Prometheus and Grafana for real-time monitoring and log aggregation.




# Deployment
We can deploy service with kubernetes pods

Deployment config file in available in deployment folder

```bash
kubectl apply -f deployment/deployment.yaml
```

This will deploy the FastAPI service, Redis, and Elasticsearch on Kubernetes.

we can access our service http://localhost:30001 as we did in local development

```bash
Swagger api doc - http://localhost:30001/api/docs
```


## Extra
We can monitor our redis queue with rq-dashboard for Redis server

```bash
rq-dashboard -u ${REDIS_URL}
```





 





















