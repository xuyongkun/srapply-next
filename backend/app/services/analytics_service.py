from datetime import datetime, timezone

from app.services.database import get_connection


class AnalyticsService:
    def add_event(
        self,
        visitor_id: str,
        event_type: str,
        page_url: str | None,
        payload: str | None,
    ) -> None:
        now = datetime.now(timezone.utc).isoformat()
        conn = get_connection()
        conn.execute(
            """
            INSERT INTO analytics_events (visitor_id, event_type, page_url, payload, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (visitor_id, event_type, page_url, payload, now),
        )
        conn.commit()

    def summary(self) -> dict:
        conn = get_connection()
        total_visitors = conn.execute(
            "SELECT COUNT(DISTINCT visitor_id) AS c FROM analytics_events"
        ).fetchone()["c"]
        consultation_visitors = conn.execute(
            "SELECT COUNT(DISTINCT visitor_id) AS c FROM leads"
        ).fetchone()["c"]
        top_pages = conn.execute(
            """
            SELECT page_url, COUNT(1) AS hits
            FROM analytics_events
            WHERE event_type = 'page_view' AND page_url IS NOT NULL
            GROUP BY page_url
            ORDER BY hits DESC
            LIMIT 10
            """
        ).fetchall()
        conversion_rate = 0.0
        if total_visitors:
            conversion_rate = round((consultation_visitors / total_visitors) * 100, 2)
        return {
            "total_visitors": int(total_visitors),
            "consultation_visitors": int(consultation_visitors),
            "conversion_rate": conversion_rate,
            "top_pages": [dict(item) for item in top_pages],
        }
