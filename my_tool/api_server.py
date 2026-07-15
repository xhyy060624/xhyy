from flask import Flask, request, jsonify
from local_usage_db import LocalUsageDB
import os

app = Flask(__name__)
db = LocalUsageDB()

# 简易鉴权：可通过环境变量设置 API_TOKEN，调用时需在 Header 中携带
API_TOKEN = os.environ.get("USAGE_DB_TOKEN", "local_dev_token")

def check_auth():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    return token == API_TOKEN

@app.before_request
def require_auth():
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401

@app.route("/summaries", methods=["POST"])
def add_summary():
    data = request.get_json()
    if not data or "user_id" not in data or "summary_text" not in data:
        return jsonify({"error": "user_id and summary_text are required"}), 400

    summary_id = db.add_summary(
        user_id=data["user_id"],
        summary_text=data["summary_text"],
        conversation_id=data.get("conversation_id"),
        tags=data.get("tags"),
        model_name=data.get("model_name")
    )
    return jsonify({"id": summary_id, "status": "stored"}), 201

@app.route("/summaries", methods=["GET"])
def get_summaries():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    limit = request.args.get("limit", 10, type=int)
    offset = request.args.get("offset", 0, type=int)
    keyword = request.args.get("keyword")

    if keyword:
        results = db.search_summaries(user_id, keyword)
    else:
        results = db.get_summaries(user_id, limit, offset)

    return jsonify(results)

@app.route("/summaries/<int:summary_id>", methods=["DELETE"])
def delete_summary(summary_id):
    success = db.delete_summary(summary_id)
    if success:
        return jsonify({"status": "deleted"}), 200
    return jsonify({"error": "not found"}), 404

if __name__ == "__main__":
    # 只监听本地，关闭 debug 模式生产更安全
    app.run(host="127.0.0.1", port=5099, debug=False)