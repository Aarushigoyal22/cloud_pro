from flask import Flask, request, jsonify
import storage

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/notes", methods=["GET"])
def list_notes():
    notes = storage.list_notes()
    return jsonify(notes), 200


@app.route("/notes/<note_id>", methods=["GET"])
def get_note(note_id):
    note = storage.get_note(note_id)
    if not note:
        return jsonify({"error": "Note not found"}), 404
    return jsonify(note), 200


@app.route("/notes", methods=["POST"])
def create_note():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({"error": "title and content are required"}), 400

    note = storage.create_note(title, content)
    return jsonify(note), 201


@app.route("/notes/<note_id>", methods=["PUT"])
def update_note(note_id):
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    content = data.get("content")

    note = storage.update_note(note_id, title=title, content=content)
    if not note:
        return jsonify({"error": "Note not found"}), 404
    return jsonify(note), 200


@app.route("/notes/<note_id>", methods=["DELETE"])
def delete_note(note_id):
    deleted = storage.delete_note(note_id)
    if not deleted:
        return jsonify({"error": "Note not found"}), 404
    return jsonify({"message": "Note deleted"}), 200


# optional: root route so browser / doesn't 404
@app.route("/", methods=["GET"])
def root():
    return jsonify(
        {
            "message": "Cloud Notes API running",
            "endpoints": ["/health", "/notes"],
        }
    ), 200


if __name__ == "__main__":
    # IMPORTANT: PORT 3000 as you asked
    app.run(host="0.0.0.0", port=3000, debug=True)
