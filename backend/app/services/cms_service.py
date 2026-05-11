from datetime import datetime, timezone

from app.services.database import get_connection


class CmsService:
    def list_cases(self) -> list[dict]:
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM cms_cases ORDER BY id DESC"
        ).fetchall()
        return [dict(r) for r in rows]

    def create_case(self, title: str, summary: str, country: str, major: str) -> int:
        now = datetime.now(timezone.utc).isoformat()
        conn = get_connection()
        cursor = conn.execute(
            """
            INSERT INTO cms_cases (title, summary, country, major, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (title, summary, country, major, now),
        )
        conn.commit()
        return int(cursor.lastrowid)

    def list_advisors(self) -> list[dict]:
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM cms_advisors ORDER BY id DESC"
        ).fetchall()
        return [dict(r) for r in rows]

    def create_advisor(self, name: str, title: str, bio: str, specialties: str) -> int:
        now = datetime.now(timezone.utc).isoformat()
        conn = get_connection()
        cursor = conn.execute(
            """
            INSERT INTO cms_advisors (name, title, bio, specialties, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, title, bio, specialties, now),
        )
        conn.commit()
        return int(cursor.lastrowid)
