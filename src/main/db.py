import psycopg2
from typing import Any, Dict, Optional, Sequence


def fetch_solicitud(
    creds: Dict[str, Any],
    tipo_solicitud: Optional[str],
    prioridad: Optional[str],
) -> Optional[Sequence[Any]]:
    """
    Ejecuta la consulta principal usando las credenciales de Secrets Manager.
    Devuelve la primera fila o None si no hay resultados.
    """
    conn = psycopg2.connect(
        host=creds["host"],
        database=creds["dbname"],
        user=creds["username"],
        password=creds["password"],
        port=creds["port"],
    )

    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT nombre_solicitante from solicitudes WHERE tipo_solicitud = %s AND prioridad = %s;",
                (tipo_solicitud, prioridad),
            )
            return cur.fetchone()
    finally:
        conn.close()
