from datetime import datetime, timezone

from app.services.database import get_connection


class LeadService:
    def upsert_from_chat(
        self,
        visitor_id: str,
        message: str,
        page_url: str | None,
        notified_wechat: bool,
    ) -> int:
        now = datetime.now(timezone.utc).isoformat()
        conn = get_connection()

        row = conn.execute(
            "SELECT id, first_message, notified_wechat FROM leads WHERE visitor_id = ? ORDER BY id DESC LIMIT 1",
            (visitor_id,),
        ).fetchone()

        if row:
            lead_id = row["id"]
            merged_notified = bool(row["notified_wechat"]) or notified_wechat
            conn.execute(
                """
                UPDATE leads
                SET latest_message = ?, page_url = ?, notified_wechat = ?, updated_at = ?
                WHERE id = ?
                """,
                (message, page_url, int(merged_notified), now, lead_id),
            )
            self.add_chat_message(lead_id=lead_id, visitor_id=visitor_id, role="user", message=message)
            conn.commit()
            return int(lead_id)

        cursor = conn.execute(
            """
            INSERT INTO leads (
                visitor_id, first_message, latest_message, page_url, status, notified_wechat, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, 'new', ?, ?, ?)
            """,
            (visitor_id, message, message, page_url, int(notified_wechat), now, now),
        )
        lead_id = int(cursor.lastrowid)
        self.add_chat_message(lead_id=lead_id, visitor_id=visitor_id, role="user", message=message)
        conn.commit()
        return lead_id

    def add_chat_message(self, lead_id: int, visitor_id: str, role: str, message: str) -> None:
        now = datetime.now(timezone.utc).isoformat()
        conn = get_connection()
        conn.execute(
            """
            INSERT INTO chat_messages (lead_id, visitor_id, role, message, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (lead_id, visitor_id, role, message, now),
        )
        conn.commit()

    def list_chat_messages(self, lead_id: int) -> list[dict]:
        conn = get_connection()
        rows = conn.execute(
            """
            SELECT id, lead_id, visitor_id, role, message, created_at
            FROM chat_messages
            WHERE lead_id = ?
            ORDER BY id ASC
            """,
            (lead_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    def list_leads(self) -> list[dict]:
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM leads ORDER BY updated_at DESC, id DESC"
        ).fetchall()
        return [dict(r) for r in rows]

    def update_status(self, lead_id: int, status: str) -> bool:
        now = datetime.now(timezone.utc).isoformat()
        conn = get_connection()
        cursor = conn.execute(
            "UPDATE leads SET status = ?, updated_at = ? WHERE id = ?",
            (status, now, lead_id),
        )
        conn.commit()
        return cursor.rowcount > 0

    def assign_lead(self, lead_id: int, assigned_to: str) -> bool:
        now = datetime.now(timezone.utc).isoformat()
        conn = get_connection()
        cursor = conn.execute(
            "UPDATE leads SET assigned_to = ?, updated_at = ? WHERE id = ?",
            (assigned_to, now, lead_id),
        )
        conn.commit()
        return cursor.rowcount > 0
