import os
import sqlite3
from pathlib import Path

_conn: sqlite3.Connection | None = None


def get_db_path() -> Path:
    if env_path := os.getenv("SRAPPLY_DB_PATH"):
        return Path(env_path)
    base_dir = Path(__file__).resolve().parents[2]
    return base_dir / "data.db"


def get_connection() -> sqlite3.Connection:
    global _conn
    if _conn is not None:
        return _conn
    _conn = sqlite3.connect(str(get_db_path()), timeout=10, check_same_thread=False)
    _conn.row_factory = sqlite3.Row
    _conn.execute("PRAGMA foreign_keys = ON")
    _conn.execute("PRAGMA journal_mode = WAL")
    init_db(_conn)
    return _conn


def close_db() -> None:
    global _conn
    if _conn is not None:
        _conn.close()
        _conn = None


def _seed_cms_data(conn: sqlite3.Connection) -> None:
    count = conn.execute("SELECT COUNT(1) AS c FROM cms_cases").fetchone()["c"]
    if count:
        return

    import datetime

    now = datetime.datetime.utcnow().isoformat()

    conn.executemany(
        "INSERT INTO cms_cases (title, summary, country, major, created_at) VALUES (?, ?, ?, ?, ?)",
        [
            ("陈同学 — 湖北美术学院 → 爱丁堡大学 + 伦敦艺术大学",
             "陈同学本科就读于湖北美术学院，希望跨专业申请英国顶尖艺术院校。顾问团队为其深度挖掘个人作品集亮点，精准匹配院校风格，最终同时斩获爱丁堡大学与伦敦艺术大学录取。",
             "英国", "艺术设计", now),
            ("刘同学 — 吉林大学 → 伦敦国王学院 + 巴斯大学",
             "刘同学来自吉林大学政治学专业，目标英国G5及顶尖政治经济学项目。顾问团队在文书打磨与科研经历提炼上重点发力，助其获得KCL与巴斯大学双录取。",
             "英国", "政治经济学", now),
            ("杨同学 — 广西大学 → 利兹大学 + 伯明翰大学",
             "杨同学本科就读于广西大学，GPA不占优势。顾问团队通过精准的选校策略和文书包装，突出其实习经历与专业匹配度，成功收获利兹大学与伯明翰大学录取。",
             "英国", "商科", now),
            ("杨同学 — 河北民族师范学院 → 都柏林大学 + 高威大学 + 利默瑞克大学",
             "双非院校背景申请爱尔兰管理学，顾问团队通过深度背景挖掘与个性化文书，帮助学生斩获三所爱尔兰名校录取，实现留学梦想。",
             "爱尔兰", "管理学", now),
            ("游同学 — 四川大学 → 伦敦国王学院",
             "游同学来自四川大学，目标直指伦敦国王学院。顾问团队精心规划申请时间线，在语言成绩、文书与推荐信三方同步推进，最终成功获得KCL录取。",
             "英国", "金融", now),
            ("王同学 — 湖北经济学院 → 悉尼大学 + 昆士兰大学",
             "王同学本科就读于湖北经济学院，希望赴澳洲攻读商科硕士。顾问团队为其量身定制申请方案，最终同时获得悉尼大学与昆士兰大学录取。",
             "澳大利亚", "商科", now),
        ],
    )

    conn.executemany(
        "INSERT INTO cms_advisors (name, title, bio, specialties, created_at) VALUES (?, ?, ?, ?, ?)",
        [
            ("Sherry", "联合创始人",
             "9年留学行业经验，曾任职于上海多家顶尖留学机构。擅长美国、英国、澳大利亚、加拿大、新加坡等国家高端申请，尤其精通挂科、绩点低等各类特殊案例的逆袭方案制定，深受学生信赖。",
             "美国,英国,澳洲,加拿大,新加坡,特殊案例", now),
            ("Rainsea", "联合创始人",
             "6年留学咨询经验，专注美国、英国、澳大利亚、加拿大、新加坡留学指导。擅长帮助学生进行院校与专业选择，结合学生兴趣与职业规划制定最优申请策略，服务细致周到。",
             "美国,英国,澳洲,加拿大,新加坡,职业规划", now),
            ("Dean", "联合创始人",
             "10年留学行业深耕，硕士学历背景。主攻美国、英国、香港、新加坡等地区高端申请，尤其擅长个性化方案定制，善于挖掘学生独特优势，打造差异化申请文书。",
             "美国,英国,香港,新加坡,高端申请,文书定制", now),
            ("Jerky", "联合创始人",
             "10年留学服务经验，主要方向为英国与澳大利亚。签证指导经验极为丰富，从业至今保持零拒签记录。以严谨细致的工作风格赢得学生与家长的一致好评。",
             "英国,澳洲,签证指导", now),
        ],
    )

    conn.commit()


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor_id TEXT NOT NULL,
            first_message TEXT NOT NULL,
            latest_message TEXT NOT NULL,
            page_url TEXT,
            status TEXT NOT NULL DEFAULT 'new',
            assigned_to TEXT,
            notified_wechat INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER NOT NULL,
            visitor_id TEXT NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (lead_id) REFERENCES leads(id)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS cms_cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            summary TEXT NOT NULL,
            country TEXT NOT NULL,
            major TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS cms_advisors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            title TEXT NOT NULL,
            bio TEXT NOT NULL,
            specialties TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS analytics_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            page_url TEXT,
            payload TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_chat_messages_lead_id ON chat_messages(lead_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_analytics_event_type ON analytics_events(event_type)")
    conn.commit()
    _seed_cms_data(conn)
