def estado_desde_status(status, punch) -> str:
    try:
        s = int(status)
        p = int(punch)
    except Exception:
        return "Descanso"

    if s == 1 and p == 0:
        return "Entrada"
    if s == 1 and p == 1:
        return "Salida"
    if s == 1 and p > 1:
        return "Descanso"
    return "Descanso"
