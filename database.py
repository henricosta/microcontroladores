import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "sensores.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sensores (
            id_sensor TEXT PRIMARY KEY,
            valor TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_sensor TEXT NOT NULL,
            valor TEXT,
            parking_lot TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    for i in range(1, 21):
        sensor_id = f"P{i}"
        cur.execute(
            "INSERT OR IGNORE INTO sensores (id_sensor, valor) VALUES (?, ?)",
            (sensor_id, 0),
        )

    conn.commit()
    conn.close()


init_db()
