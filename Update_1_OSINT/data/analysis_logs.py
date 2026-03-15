"""
Analysis Logs Database
======================
SQLite database handler for OSINT SOC / SIEM platform

IMPORTANT:
• Uses centralized DB_PATH from data/db_config.py
• Do NOT redefine DB paths here
"""

import sqlite3
from datetime import datetime

# ✅ SINGLE SOURCE OF TRUTH
from data.db_config import DB_PATH


# ================= DB INIT =================
def init_db():
    """
    Create analysis_logs table if not exists
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS analysis_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target TEXT NOT NULL,
        threat_level TEXT NOT NULL,
        threat_type TEXT,
        risk_score INTEGER,
        vt_score INTEGER,
        abuse_score INTEGER,
        open_ports TEXT,
        suggestion TEXT,
        greynoise_score INTEGER,
        alienvault_score INTEGER,
        urlscan_uuid TEXT,
        mitigation_playbook TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS campaigns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS watchlists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campaign_id INTEGER,
        target TEXT NOT NULL,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(campaign_id) REFERENCES campaigns(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS webhooks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        url TEXT NOT NULL,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Attempt to add columns if updating an existing DB (SQLite ALTER TABLE support is limited, so we catch errors)
    columns = [
        ('greynoise_score', 'INTEGER'),
        ('alienvault_score', 'INTEGER'),
        ('urlscan_uuid', 'TEXT'),
        ('mitigation_playbook', 'TEXT')
    ]
    for col_name, col_type in columns:
        try:
            cur.execute(f'ALTER TABLE analysis_logs ADD COLUMN {col_name} {col_type}')
        except sqlite3.OperationalError:
            pass

    conn.commit()
    conn.close()


# ================= INSERT LOG =================
def insert_log(
    target: str,
    threat_level: str,
    threat_type: str,
    risk_score: int,
    vt_score: int = 0,
    abuse_score: int = 0,
    open_ports: str = "",
    suggestion: str = "",
    greynoise_score: int = 0,
    alienvault_score: int = 0,
    urlscan_uuid: str = "",
    mitigation_playbook: str = ""
):
    """
    Insert one analysis record into database
    """

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO analysis_logs
    (
        target,
        threat_level,
        threat_type,
        risk_score,
        vt_score,
        abuse_score,
        open_ports,
        suggestion,
        greynoise_score,
        alienvault_score,
        urlscan_uuid,
        mitigation_playbook,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        target,
        threat_level,
        threat_type,
        risk_score,
        vt_score,
        abuse_score,
        open_ports,
        suggestion,
        greynoise_score,
        alienvault_score,
        urlscan_uuid,
        mitigation_playbook,
        datetime.utcnow()
    ))

    conn.commit()
    conn.close()


# ================= FETCH ALL =================
def fetch_logs(limit: int = 100):
    """
    Fetch latest analysis logs
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    SELECT *
    FROM analysis_logs
    ORDER BY created_at DESC
    LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()
    return rows


# ================= FILTER LOGS =================
def filter_logs(threat_level: str | None = None, target: str | None = None):
    """
    Filter logs by threat level and/or target
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    query = "SELECT * FROM analysis_logs WHERE 1=1"
    params = []

    if threat_level and threat_level.lower() != "all":
        query += " AND threat_level = ?"
        params.append(threat_level)

    if target:
        query += " AND target LIKE ?"
        params.append(f"%{target}%")

    query += " ORDER BY created_at DESC"

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows


# ================= DASHBOARD ANALYTICS =================
def get_threat_counts():
    """
    Count threats by severity
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    SELECT threat_level, COUNT(*)
    FROM analysis_logs
    GROUP BY threat_level
    """)

    data = cur.fetchall()
    conn.close()

    counts = {
        "Low Risk": 0,
        "Medium Risk": 0,
        "High Risk": 0
    }

    for level, count in data:
        counts[level] = count

    return counts


def get_abuse_timeline(limit: int = 10):
    """
    Abuse score timeline for charts
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    SELECT created_at, abuse_score
    FROM analysis_logs
    ORDER BY created_at DESC
    LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()

    labels = [row[0][:10] for row in reversed(rows)]
    values = [row[1] for row in reversed(rows)]

    return {
        "labels": labels,
        "values": values
    }


# ================= AUTO INIT =================
init_db()
