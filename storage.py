import json
import os
import threading
from datetime import datetime
import uuid

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "notes.json")
_lock = threading.Lock()  # for thread-safe access


def _ensure_storage():
    """Ensure data directory and JSON file exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)


def _read_all():
    _ensure_storage()
    with _lock:
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # if file corrupted, reset it
                return []


def _write_all(notes):
    with _lock:
        with open(DATA_FILE, "w") as f:
            json.dump(notes, f, indent=2)


def list_notes():
    return _read_all()


def get_note(note_id: str):
    notes = _read_all()
    for n in notes:
        if n["id"] == note_id:
            return n
    return None


def create_note(title: str, content: str):
    notes = _read_all()
    now = datetime.utcnow().isoformat() + "Z"
    note = {
        "id": str(uuid.uuid4()),
        "title": title,
        "content": content,
        "created_at": now,
        "updated_at": now,
    }
    notes.append(note)
    _write_all(notes)
    return note


def update_note(note_id: str, title=None, content=None):
    notes = _read_all()
    updated = None
    for n in notes:
        if n["id"] == note_id:
            if title is not None:
                n["title"] = title
            if content is not None:
                n["content"] = content
            n["updated_at"] = datetime.utcnow().isoformat() + "Z"
            updated = n
            break
    if updated:
        _write_all(notes)
    return updated


def delete_note(note_id: str) -> bool:
    notes = _read_all()
    new_notes = [n for n in notes if n["id"] != note_id]
    if len(new_notes) == len(notes):
        return False
    _write_all(new_notes)
    return True
