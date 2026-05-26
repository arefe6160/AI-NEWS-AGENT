import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "seen_videos.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS seen_videos (
            video_id TEXT PRIMARY KEY,
            title TEXT,
            seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def is_seen(video_id: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT 1 FROM seen_videos WHERE video_id = ?", (video_id,)
    ).fetchone()
    conn.close()
    return row is not None

def mark_seen(video_id: str, title: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT OR IGNORE INTO seen_videos (video_id, title) VALUES (?, ?)",
        (video_id, title)
    )
    conn.commit()
    conn.close()