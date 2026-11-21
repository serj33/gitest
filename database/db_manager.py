import json
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parent / "modeusaristo.db"


def _connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with _connect() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profession TEXT NOT NULL DEFAULT 'general',
            payload TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS persona (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            payload TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS interview_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS expert_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)


def save_facts(facts: list, profession: str = "general"):
    with _connect() as conn:
        conn.execute("DELETE FROM facts WHERE profession = ?", (profession,))
        conn.executemany(
            "INSERT INTO facts (profession, payload) VALUES (?, ?)",
            [(profession, json.dumps(fact, ensure_ascii=False)) for fact in facts]
        )


def get_facts(profession: str | None = None) -> list[dict[str, Any]]:
    with _connect() as conn:
        if profession:
            rows = conn.execute(
                "SELECT payload FROM facts WHERE profession = ? ORDER BY id", (profession,)
            ).fetchall()
        else:
            rows = conn.execute("SELECT payload FROM facts ORDER BY id").fetchall()
    return [json.loads(row["payload"]) for row in rows]


def save_persona(persona: dict):
    with _connect() as conn:
        conn.execute(
            "INSERT INTO persona (id, payload, updated_at) VALUES (1, ?, CURRENT_TIMESTAMP) "
            "ON CONFLICT(id) DO UPDATE SET payload=excluded.payload, updated_at=CURRENT_TIMESTAMP",
            (json.dumps(persona, ensure_ascii=False),)
        )


def get_persona():
    with _connect() as conn:
        row = conn.execute("SELECT payload FROM persona WHERE id = 1").fetchone()
    return json.loads(row["payload"]) if row else None


def _save_message(table: str, role: str, content: str):
    if table not in {"interview_history", "expert_history"}:
        raise ValueError("Unsupported table")
    with _connect() as conn:
        conn.execute(f"INSERT INTO {table} (role, content) VALUES (?, ?)", (role, content))


def _get_history(table: str):
    with _connect() as conn:
        rows = conn.execute(f"SELECT role, content FROM {table} ORDER BY id").fetchall()
    return [dict(row) for row in rows]


def _clear_history(table: str):
    if table not in {"interview_history", "expert_history"}:
        raise ValueError("Unsupported table")
    with _connect() as conn:
        conn.execute(f"DELETE FROM {table}")


def save_interview_message(role, content): _save_message("interview_history", role, content)
def get_interview_history(): return _get_history("interview_history")
def clear_interview_history(): _clear_history("interview_history")
def save_expert_message(role, content): _save_message("expert_history", role, content)
def get_expert_history(): return _get_history("expert_history")
def clear_expert_history(): _clear_history("expert_history")


init_db()
