from passlib.hash import bcrypt

from app.services.database import get_connection

_seeded = False


def _seed_admin_users() -> None:
    global _seeded
    if _seeded:
        return
    conn = get_connection()
    count = conn.execute("SELECT COUNT(1) AS c FROM admin_users").fetchone()["c"]
    if count:
        _seeded = True
        return
    conn.executemany(
        "INSERT INTO admin_users (username, password, role) VALUES (?, ?, ?)",
        [
            ("admin", bcrypt.hash("admin123"), "admin"),
            ("consultant", bcrypt.hash("consult123"), "consultant"),
            ("operator", bcrypt.hash("oper123"), "operator"),
        ],
    )
    conn.commit()
    _seeded = True


class UserService:
    def __init__(self) -> None:
        _seed_admin_users()

    def get_user(self, username: str) -> dict | None:
        conn = get_connection()
        row = conn.execute(
            "SELECT id, username, password, role FROM admin_users WHERE username = ?",
            (username,),
        ).fetchone()
        return dict(row) if row else None

    def list_users(self) -> list[dict]:
        conn = get_connection()
        rows = conn.execute(
            "SELECT id, username, role FROM admin_users ORDER BY id ASC"
        ).fetchall()
        return [dict(r) for r in rows]
