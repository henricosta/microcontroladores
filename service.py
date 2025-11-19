import datetime
from database import get_connection


def get_last_state(id_sensor: str | None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT valor, updated_at FROM sensores WHERE id_sensor = ?",
        (id_sensor,),
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def save_state(id_sensor: str | None, valor: float, parking_lot: str | None = None):
    last = get_last_state(id_sensor)
    if last and str(last["valor"]) == str(valor):
        return False

    conn = get_connection()
    cur = conn.cursor()

    if last:
        cur.execute(
            "UPDATE sensores SET valor=?, updated_at=CURRENT_TIMESTAMP WHERE id_sensor = ?",
            (valor, id_sensor),
        )
    else:
        cur.execute(
            "INSERT INTO sensores (id_sensor, valor) VALUES (?, ?)", (id_sensor, valor)
        )

    cur.execute(
        "INSERT INTO historico (id_sensor, valor, parking_lot) VALUES (?, ?, ?)",
        (id_sensor, valor, parking_lot),
    )

    conn.commit()
    conn.close()
    return True


def get_history(id_sensor: str | None = None):
    conn = get_connection()
    cur = conn.cursor()
    if id_sensor:
        cur.execute(
            "SELECT * FROM historico WHERE id_sensor = ? ORDER BY timestamp DESC LIMIT 20",
            (id_sensor,),
        )
    else:
        cur.execute("SELECT * FROM historico ORDER BY timestamp DESC LIMIT 20")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_occupation_time(id_sensor: str | None):
    state = get_last_state(id_sensor)
    if not state or state["valor"] == 0:
        return {"ocupado": False, "tempo_ocupado_segundos": 0}

    last_time = datetime.datetime.fromisoformat(state["updated_at"])
    now = datetime.datetime.now()
    delta = (now - last_time).total_seconds()
    return {"ocupado": True, "tempo_ocupado_segundos": int(delta)}


def get_total_sensors():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS total FROM sensores")
    total = cur.fetchone()[0]
    conn.close()
    return total


def get_all_sensors():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id_sensor, valor, updated_at FROM sensores")
    rows = cur.fetchall()
    conn.close()

    sensors_map = {r["id_sensor"]: r for r in rows}

    sensors = []
    for i in range(1, 21):
        sensor_id = f"P{i}"
        state = sensors_map.get(sensor_id)
        if state:
            sensors.append(
                {"id_sensor": sensor_id, "valor": state["valor"], "tempo_ocupado": None}
            )
        else:
            sensors.append(
                {
                    "id_sensor": sensor_id,
                    "valor": None,
                    "tempo_ocupado": "Não instalado",
                }
            )
    return sensors
