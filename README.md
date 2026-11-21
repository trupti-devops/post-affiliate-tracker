# Post & Affiliate Link Tracker

A small Flask API to store social media posts and count clicks on their affiliate links.

## Tech
Python (Flask), Docker, Kubernetes (Minikube)

## API
- `POST /posts` adds a post (title, platform, link)
- `GET /posts` lists all posts
- `GET /go/<id>` counts a click and redirects to the affiliate link

## Run with Docker
    docker build -t post-tracker:v1 .
    docker run -p 5000:5000 post-tracker:v1

## Deploy on Kubernetes (Minikube)
    minikube image load post-tracker:v1
    kubectl apply -f k8s/
    minikube service post-tracker --url

## Notes
Data is stored in a file inside the container, so the Deployment uses 1 replica. A database or persistent volume is the next improvement.
