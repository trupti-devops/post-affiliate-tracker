from flask import Flask, request, jsonify, redirect
import json, os

app = Flask(__name__)
DATA_FILE = "data.json"

def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return []

def save(items):
    with open(DATA_FILE, "w") as f:
        json.dump(items, f)

@app.route("/")
def home():
    return "Post & Affiliate Link Tracker is running!"

@app.route("/posts", methods=["GET"])
def list_posts():
    return jsonify(load())

@app.route("/posts", methods=["POST"])
def add_post():
    data = request.get_json()
    items = load()
    item = {"id": len(items) + 1, "title": data["title"],
            "platform": data["platform"], "link": data["link"], "clicks": 0}
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
