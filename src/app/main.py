import os
import shutil
from datetime import datetime
from openpyxl import Workbook

from .config import load_settings
from .paths import ensure_dir, safe_join
from .excel_out import export_eventos_xlsx, export_resumen_xlsx, load_demo_events
from .timeparse import parse_date_generic, parse_time_generic
from .payroll import calcular_horas_desde_excel, escribir_hoja_resumen, escribir_hoja_diario

# PROD
from .zkteco_prod import obtener_ip_por_mac, descargar_eventos_zkteco
from .zktime_db import cargar_empleados

def _crear_excel_limpio_desde_rows(rows_limpias: list[tuple], out_path: str) -> str:
    """
    rows_limpias: (Nombre, Fecha, Hora, Estado)
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "EventosLimpios"
    ws.append(["Nombre", "Fecha", "Hora", "Estado"])
    for r in rows_limpias:
        ws.append(list(r))
    wb.save(out_path)
    return out_path

def run_demo(settings):
    ensure_dir(settings.local_out)

    demo_path = os.path.join("data", "sample_events.xlsx")
    items = load_demo_events(demo_path)

    # convertir a (Nombre, Fecha(date), Hora(time), Estado)
    rows_limpias = []
    for it in items:
        nombre = str(it["nombre"]).strip()
        fecha = parse_date_generic(it["fecha"])
        hora = parse_time_generic(it["hora"])
        estado = str(it["estado"]).strip()
        if nombre and fecha and hora and estado:
            rows_limpias.append((nombre, fecha, hora, estado))

    tag = datetime.now().strftime("%Y%m%d_%H%M%S")
    path_clean = os.path.join(settings.local_out, f"Eventos_Limpios_DEMO_{tag}.xlsx")
    _crear_excel_limpio_desde_rows(rows_limpias, path_clean)

    # quincena: por defecto, detecta mes actual y quincena 1
    now = datetime.now()
    year, month, quincena = now.year, now.month, 1

    quincena_rows, diario_rows, _rango = calcular_horas_desde_excel(
        path_clean, year, month, quincena, settings.margen_dias_quincena
    )

    out_res = os.path.join(settings.local_out, f"Resumen_Horas_DEMO_{tag}.xlsx")
    export_resumen_xlsx(out_res, quincena_rows, diario_rows, escribir_hoja_resumen, escribir_hoja_diario)
    print(f"[DEMO] Generado: {out_res}")

def run_prod(settings):
    if not (settings.zk_mac and settings.zk_net_prefix and settings.zktime_db_path):
        raise RuntimeError("Faltan variables PROD (ZK_MAC, ZK_NET_PREFIX, ZKTIME_DB_PATH).")

    ensure_dir(settings.local_out)
    ensure_dir(settings.tesoreria_out)

    ip = obtener_ip_por_mac(settings.zk_mac, settings.zk_net_prefix)
    if not ip:
        raise RuntimeError("No se encontró el reloj en la red.")

    empleados = cargar_empleados(settings.zktime_db_path)
    eventos = descargar_eventos_zkteco(ip, settings.dias_atras)

    # construir rows para Excel eventos
    rows_eventos = []
    rows_limpias = []
    for ev in eventos:
        pin = ev["pin"]
        ts = ev["timestamp"]
        estado = ev["estado"]
        empleado = empleados.get(pin, f"PIN {pin}")

        fecha = ts.date()
        hora = ts.time()

        rows_eventos.append((pin, empleado, fecha.strftime("%Y-%m-%d"), hora.strftime("%H:%M:%S"), estado))
        rows_limpias.append((empleado, fecha, hora, estado))

    tag = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 1) Excel eventos
    eventos_name = f"Eventos_{tag}.xlsx"
    eventos_local = safe_join(settings.local_out, eventos_name)
    export_eventos_xlsx(eventos_local, rows_eventos)

    # copia a tesorería
    try:
        shutil.copy2(eventos_local, safe_join(settings.tesoreria_out, eventos_name))
    except Exception as e:
        print(f"[WARN] No se pudo copiar eventos a tesorería: {e}")

    # 2) Excel limpio temporal
    clean_path = safe_join(settings.local_out, f"Eventos_Limpios_{tag}.xlsx")
    _crear_excel_limpio_desde_rows(rows_limpias, clean_path)

    # 3) Resumen quincena
    now = datetime.now()
    year, month, quincena = now.year, now.month, 1  # aquí puedes definir quincena por fecha
    quincena_rows, diario_rows, _rango = calcular_horas_desde_excel(
        clean_path, year, month, quincena, settings.margen_dias_quincena
    )

    resumen_name = f"Resumen_Horas_{tag}.xlsx"
    resumen_local = safe_join(settings.local_out, resumen_name)

    export_resumen_xlsx(resumen_local, quincena_rows, diario_rows, escribir_hoja_resumen, escribir_hoja_diario)
    try:
        shutil.copy2(resumen_local, safe_join(settings.tesoreria_out, resumen_name))
    except Exception as e:
        print(f"[WARN] No se pudo copiar resumen a tesorería: {e}")

    print("[PROD] OK")

def main():
    settings = load_settings()
    mode = settings.app_mode.upper()

    if mode == "DEMO":
        run_demo(settings)
    elif mode == "PROD":
        run_prod(settings)
    else:
        raise RuntimeError("APP_MODE debe ser DEMO o PROD.")

if __name__ == "__main__":
    main()
