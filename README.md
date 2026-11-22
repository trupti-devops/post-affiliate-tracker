# Post & Affiliate Link Tracker

A Flask API that stores social media posts and counts clicks on their affiliate links, with a simple dashboard.

## Features
- Add posts, protected by an API key
- Tracking link `/go/<id>` counts the click, then redirects to the affiliate link
- Dashboard page with a table of posts and clicks
- Data kept in a Docker volume, so it survives restarts

## API
- `GET /` health check
- `POST /posts` adds a post (header `X-API-Key`)
- `GET /posts` lists all posts
- `GET /go/<id>` counts a click and redirects
- `GET /dashboard?key=<API_KEY>` shows the dashboard

## Run with Docker
    docker build -t post-tracker:v2 .
    docker run -p 5000:5000 -e API_KEY=<your-secret> -e DATA_FILE=/data/data.json -v post-data:/data post-tracker:v2

## CI
GitHub Actions builds the Docker image and pushes it to Docker Hub on every push to `main`.

## Kubernetes
Manifests are in `k8s/` (tested on Minikube).

## Next steps
Deploy on AWS EC2, and move storage to a database.
