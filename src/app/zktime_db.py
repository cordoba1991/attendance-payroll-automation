import sqlite3

def cargar_empleados(db_path: str) -> dict[str, str]:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT emp_pin, emp_firstname, emp_lastname FROM hr_employee")
    empleados = {
        str(row[0]): f"{(row[1] or '').strip()} {(row[2] or '').strip()}".strip()
        for row in cur.fetchall()
    }
    conn.close()
    return empleados
