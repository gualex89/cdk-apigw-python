import psycopg2
from typing import Any, Dict, Optional, Sequence


def fetch_solicitud(
    creds: Dict[str, Any],
    tipo_solicitud: Optional[str],
    prioridad: Optional[str],
) -> Optional[Sequence[Dict[str, Any]]]:
    """
    Ejecuta la consulta principal usando las credenciales de Secrets Manager.
    Devuelve todas las filas como diccionarios o None si no hay resultados.
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
                "SELECT * FROM solicitudes WHERE tipo_solicitud = %s AND prioridad = %s ORDER BY id;",
                (tipo_solicitud, prioridad),
            )
            columns = [desc[0] for desc in cur.description]  # Obtener nombres de columnas
            rows = cur.fetchall()  # Obtener todas las filas

            # Convertir filas a diccionarios
            return [dict(zip(columns, row)) for row in rows] if rows else None
    finally:
        conn.close()