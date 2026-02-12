import subprocess
from datetime import datetime, timedelta
from zk import ZK
from .events import estado_desde_status

def obtener_ip_por_mac(mac_reloj: str, net_prefix: str) -> str | None:
    mac_target = mac_reloj.lower().strip()
    for i in range(1, 255):
        ip = f"{net_prefix}{i}"

        subprocess.run(["ping", "-n", "1", "-w", "80", ip],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        res = subprocess.run(["arp", "-a", ip],
                             capture_output=True, text=True, errors="ignore")

        if mac_target in (res.stdout or "").lower():
            return ip
    return None

def descargar_eventos_zkteco(ip: str, dias_atras: int) -> list[dict]:
    """
    Devuelve lista de dicts:
    { "pin": "123", "timestamp": datetime, "estado": "Entrada/Salida/Descanso" }
    """
    zk = ZK(ip, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
    conn = None
    try:
        conn = zk.connect()
        conn.disable_device()

        desde = datetime.now() - timedelta(days=dias_atras)
        atts = conn.get_attendance() or []

        eventos = []
        for a in atts:
            # a.user_id / a.timestamp / a.status / a.punch
            if a.timestamp < desde:
                continue
            eventos.append({
                "pin": str(a.user_id),
                "timestamp": a.timestamp,
                "estado": estado_desde_status(getattr(a, "status", None), getattr(a, "punch", None)),
            })
        return eventos
    finally:
        if conn:
            try:
                conn.enable_device()
            except Exception:
                pass
            try:
                conn.disconnect()
            except Exception:
                pass
