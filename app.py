from flask import Flask, request, jsonify, redirect
from html import escape
import json
import os

app = Flask(__name__)

DATA_FILE = os.environ.get("DATA_FILE", "data.json")
API_KEY = os.environ.get("API_KEY", "")


def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return []


def save(items):
    folder = os.path.dirname(DATA_FILE)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(items, f)


def key_ok(supplied):
    return bool(API_KEY) and supplied == API_KEY


@app.route("/")
def home():
    return "Post & Affiliate Link Tracker is running!"


@app.route("/posts", methods=["GET"])
def list_posts():
    return jsonify(load())


@app.route("/posts", methods=["POST"])
def add_post():
    if not key_ok(request.headers.get("X-API-Key")):
        return jsonify({"error": "unauthorized"}), 401
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    platform = data.get("platform")
    link = str(data.get("link", ""))
    if not title or not platform or not link.startswith(("http://", "https://")):
        return jsonify({"error": "title, platform and a link starting with http:// or https:// are required"}), 400
    items = load()
    item = {"id": len(items) + 1, "title": title, "platform": platform, "link": link, "clicks": 0}
    items.append(item)
    save(items)
    return jsonify(item), 201


@app.route("/go/<int:post_id>")
def go(post_id):
    items = load()
    for item in items:
        if item["id"] == post_id:
            item["clicks"] += 1
            save(items)
            return redirect(item["link"])
    return "Not found", 404


@app.route("/dashboard")
def dashboard():
    if not key_ok(request.args.get("key")):
        return "Unauthorized", 401
    items = load()
    total = sum(p["clicks"] for p in items)
    page = "<html><head><title>Tracker Dashboard</title></head>"
    page += "<body style='font-family:sans-serif;padding:20px'>"
    page += "<h2>Post &amp; Affiliate Link Tracker</h2>"
    page += "<p>Total clicks: <b>" + str(total) + "</b></p>"
    page += "<table border='1' cellpadding='8' style='border-collapse:collapse'>"
    page += "<tr><th>ID</th><th>Title</th><th>Platform</th><th>Clicks</th><th>Tracking link</th></tr>"
    for p in items:
        page += "<tr><td>" + str(p["id"]) + "</td><td>" + escape(str(p["title"])) + "</td><td>" + escape(str(p["platform"])) + "</td><td>" + str(p["clicks"]) + "</td><td>/go/" + str(p["id"]) + "</td></tr>"
    page += "</table></body></html>"
    return page


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
