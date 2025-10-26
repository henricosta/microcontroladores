import datetime
from database import get_connection, init_db

init_db()

def get_last_state(id_sensor: str | None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT valor, atualizado_em FROM sensores WHERE id_sensor IS ? ORDER BY id DESC LIMIT 1",
        (id_sensor,),
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def save_state(id_sensor: str | None, valor: int):
    last = get_last_state(id_sensor)
    if last and last["valor"] == valor:
        return False

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO historico (id_sensor, valor) VALUES (?, ?)",
        (id_sensor, valor),
    )

    if last:
        cur.execute(
            "UPDATE sensores SET valor=?, atualizado_em=CURRENT_TIMESTAMP WHERE id_sensor IS ?",
            (valor, id_sensor),
        )
    else:
        cur.execute(
            "INSERT INTO sensores (id_sensor, valor) VALUES (?, ?)",
            (id_sensor, valor),
        )

    conn.commit()
    conn.close()
    return True

def get_history(id_sensor: str | None = None):
    conn = get_connection()
    cur = conn.cursor()
    if id_sensor:
        cur.execute(
            "SELECT * FROM historico WHERE id_sensor IS ? ORDER BY data_hora DESC",
            (id_sensor,),
        )
    else:
        cur.execute("SELECT * FROM historico ORDER BY data_hora DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_occupation_time(id_sensor: str | None):
    state = get_last_state(id_sensor)
    if not state or state["valor"] == 0:
        return {"ocupado": False, "tempo_ocupado_segundos": 0}

    last_time = datetime.datetime.fromisoformat(state["atualizado_em"])
    now = datetime.datetime.now()
    delta = (now - last_time).total_seconds()
    return {"ocupado": True, "tempo_ocupado_segundos": int(delta)}
