from flask import Flask, request, jsonify
from app.store import Store

app = Flask(__name__)
store = Store()

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/set", methods=["POST"])
def set_value():
    """Set a key to a given value."""
    body = request.get_json(silent=True) or {}
    key, value = body.get("key"), body.get("value")
    if key is None or value is None:
        return jsonify({"error": "Both 'key' and 'value' are required"}), 400
    store.set(key, value)
    return jsonify({"status": "ok"}), 200

@app.route("/get/<key>", methods=["GET"])
def get_value(key):
    """Get the value for a key."""
    val = store.get(key)
    if val is None:
        return jsonify({"error": f"Key '{key}' not found"}), 404
    return jsonify({"value": val}), 200

@app.route("/delete/<key>", methods=["DELETE"])
def delete_value(key):
    """Delete a key if it exists."""
    store.delete(key)
    return jsonify({"status": "ok"}), 200

@app.route("/begin", methods=["POST"])
def begin_txn():
    store.begin()
    return jsonify({"status": "transaction started"}), 200

@app.route("/commit", methods=["POST"])
def commit_txn():
    if store.commit():
        return jsonify({"status": "committed"}), 200
    return jsonify({"error": "No active transaction"}), 400

@app.route("/rollback", methods=["POST"])
def rollback_txn():
    if store.rollback():
        return jsonify({"status": "rolled back"}), 200
    return jsonify({"error": "No active transaction"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
