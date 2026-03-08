from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict


DEFAULT_PREFS = {
    "morning": 60,
    "afternoon": 70,
    "night": 25,
}


class PreferenceStore:
    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()

    def _init_db(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS room_preferences (
                room_id TEXT,
                time_bucket TEXT,
                brightness INTEGER,
                updated_at TEXT,
                PRIMARY KEY (room_id, time_bucket)
            )
            """
        )
        self.conn.commit()

    def get_room_preferences(self, room_id: str) -> Dict[str, int]:
        prefs = DEFAULT_PREFS.copy()
        cur = self.conn.execute(
            "SELECT time_bucket, brightness FROM room_preferences WHERE room_id = ?",
            (room_id,),
        )
        for time_bucket, brightness in cur.fetchall():
            prefs[time_bucket] = int(brightness)
        return prefs

    def update_preference(self, room_id: str, time_bucket: str, observed_brightness: int, alpha: float = 0.3) -> int:
        current = self.get_room_preferences(room_id)[time_bucket]
        new_value = round((1 - alpha) * current + alpha * observed_brightness)
        self.conn.execute(
            """
            INSERT INTO room_preferences (room_id, time_bucket, brightness, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(room_id, time_bucket) DO UPDATE SET
                brightness = excluded.brightness,
                updated_at = excluded.updated_at
            """,
            (room_id, time_bucket, new_value, datetime.utcnow().isoformat()),
        )
        self.conn.commit()
        return new_value
