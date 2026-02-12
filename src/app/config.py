from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    app_mode: str               # DEMO o PROD
    local_out: str
    tesoreria_out: str
    dias_atras: int
    margen_dias_quincena: int

    # PROD:
    zk_mac: str | None
    zk_net_prefix: str | None
    zktime_db_path: str | None

def _getenv(name: str, default: str | None = None) -> str | None:
    v = os.getenv(name, default)
    if v is None:
        return None
    v = str(v).strip()
    return v if v else None

def load_settings() -> Settings:
    app_mode = (_getenv("APP_MODE", "DEMO") or "DEMO").upper()

    local_out = _getenv("LOCAL_OUT", r".\output") or r".\output"
    tesoreria_out = _getenv("TESORERIA_OUT", local_out) or local_out

    dias_atras = int(_getenv("DIAS_ATRAS", "17") or "17")
    margen = int(_getenv("MARGEN_DIAS_QUINCENA", "3") or "3")

    zk_mac = _getenv("ZK_MAC")
    zk_net_prefix = _getenv("ZK_NET_PREFIX")
    zktime_db_path = _getenv("ZKTIME_DB_PATH")
    
    if app_mode == "PROD":
        missing = []
        if not zk_mac:
            missing.append("ZK_MAC")
        if not zk_net_prefix:
            missing.append("ZK_NET_PREFIX")
        if not zktime_db_path:
            missing.append("ZKTIME_DB_PATH")

        if missing:
            raise RuntimeError(f"Faltan variables para PROD: {', '.join(missing)}")


    return Settings(
        app_mode=app_mode,
        local_out=local_out,
        tesoreria_out=tesoreria_out,
        dias_atras=dias_atras,
        margen_dias_quincena=margen,
        zk_mac=zk_mac,
        zk_net_prefix=zk_net_prefix,
        zktime_db_path=zktime_db_path,
    )
