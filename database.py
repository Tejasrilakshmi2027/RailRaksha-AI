import sqlite3
from datetime import datetime

DB_NAME = "railraksha.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_type TEXT,
            message TEXT,
            severity TEXT,
            status TEXT DEFAULT 'Pending',
            officer_name TEXT DEFAULT 'Not Assigned',
            action_taken TEXT DEFAULT 'No action taken yet',
            timestamp TEXT,
            updated_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS plates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate_number TEXT,
            image_path TEXT,
            status TEXT DEFAULT 'Normal',
            timestamp TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS chatbot_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_query TEXT,
            bot_response TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


def migrate_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    alert_columns = [
        ("status", "TEXT DEFAULT 'Pending'"),
        ("officer_name", "TEXT DEFAULT 'Not Assigned'"),
        ("action_taken", "TEXT DEFAULT 'No action taken yet'"),
        ("updated_at", "TEXT")
    ]

    for column_name, column_type in alert_columns:
        try:
            c.execute(f"ALTER TABLE alerts ADD COLUMN {column_name} {column_type}")
        except sqlite3.OperationalError:
            pass

    try:
        c.execute("ALTER TABLE plates ADD COLUMN status TEXT DEFAULT 'Normal'")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()


def save_alert(alert_type, message, severity):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute("""
        INSERT INTO alerts (
            alert_type, message, severity, status,
            officer_name, action_taken, timestamp, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        alert_type,
        message,
        severity,
        "Pending",
        "Not Assigned",
        "No action taken yet",
        now,
        now
    ))

    conn.commit()
    conn.close()


def save_plate(plate_number, image_path, status="Normal"):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        INSERT INTO plates (plate_number, image_path, status, timestamp)
        VALUES (?, ?, ?, ?)
    """, (
        plate_number,
        image_path,
        status,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def save_chat(user_query, bot_response):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        INSERT INTO chatbot_logs (user_query, bot_response, timestamp)
        VALUES (?, ?, ?)
    """, (
        user_query,
        bot_response,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_alerts():
    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute("""
        SELECT
            id,
            alert_type,
            message,
            severity,
            COALESCE(status, 'Pending') AS status,
            COALESCE(officer_name, 'Not Assigned') AS officer_name,
            COALESCE(action_taken, 'No action taken yet') AS action_taken,
            timestamp,
            COALESCE(updated_at, timestamp) AS updated_at
        FROM alerts
        ORDER BY id DESC
    """).fetchall()
    conn.close()
    return rows


def get_plates():
    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute("""
        SELECT
            id,
            plate_number,
            image_path,
            COALESCE(status, 'Normal') AS status,
            timestamp
        FROM plates
        ORDER BY id DESC
    """).fetchall()
    conn.close()
    return rows


def get_chats():
    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute("""
        SELECT
            id,
            user_query,
            bot_response,
            timestamp
        FROM chatbot_logs
        ORDER BY id DESC
    """).fetchall()
    conn.close()
    return rows


def update_alert_status(alert_id, status, officer_name, action_taken):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute("""
        UPDATE alerts
        SET status = ?, officer_name = ?, action_taken = ?, updated_at = ?
        WHERE id = ?
    """, (
        status,
        officer_name,
        action_taken,
        updated_at,
        alert_id
    ))

    conn.commit()
    conn.close()