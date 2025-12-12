"""SQLite storage for transcript segments."""

import aiosqlite
from datetime import datetime
from pathlib import Path
from typing import AsyncIterator

from caption_ai.bus import Segment
from caption_ai.config import config


class Storage:
    """SQLite storage manager for segments."""

    def __init__(self, db_path: Path | None = None) -> None:
        """Initialize storage with database path."""
        self.db_path = db_path or config.storage_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    async def init(self) -> None:
        """Initialize database schema."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS segments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    text TEXT NOT NULL,
                    speaker TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            await db.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_timestamp
                ON segments(timestamp)
                """
            )
            await db.commit()

    async def append(self, segment: Segment) -> None:
        """Append a segment to storage."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT INTO segments (timestamp, text, speaker)
                VALUES (?, ?, ?)
                """
                ,
                (
                    segment.timestamp.isoformat(),
                    segment.text,
                    segment.speaker,
                ),
            )
            await db.commit()

    async def fetch_recent(
        self, limit: int = 10, since: datetime | None = None
    ) -> AsyncIterator[Segment]:
        """Fetch recent segments."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            query = "SELECT timestamp, text, speaker FROM segments"
            params: list = []

            if since:
                query += " WHERE timestamp >= ?"
                params.append(since.isoformat())

            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)

            async with db.execute(query, params) as cursor:
                async for row in cursor:
                    yield Segment(
                        timestamp=datetime.fromisoformat(row["timestamp"]),
                        text=row["text"],
                        speaker=row["speaker"],
                    )

