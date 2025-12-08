import psycopg2
from typing import Any, Dict, Optional, Sequence


def fetch_solicitud(
    creds: Dict[str, Any],
    tipo_solicitud: str,
    prioridad: str, 
    fecha_materializacion: Optional[str],
    fecha_creacion_desde: Optional[str],
    fecha_creacion_hasta: Optional[str]
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

    print(f" fecha_materializacion: {fecha_materializacion}, fecha_creacion_desde: {fecha_creacion_desde}, fecha_creacion_hasta: {fecha_creacion_hasta} ")

    try:
        with conn.cursor() as cur:
            sql = [
                "SELECT * FROM solicitudes",
                "WHERE tipo_solicitud = %s AND prioridad = %s",
            ]
            params = [tipo_solicitud, prioridad]

            if fecha_materializacion:
                sql.append("AND fecha_materializacion >= %s")
                params.append(fecha_materializacion)
    
            if fecha_creacion_desde and fecha_creacion_hasta:
                sql.append("AND fecha_creacion BETWEEN %s AND %s")
                params.extend([fecha_creacion_desde, fecha_creacion_hasta])

            sql.append("ORDER BY id;")

            cur.execute(" ".join(sql), params)
            columns = [desc[0] for desc in cur.description]  # Obtener nombres de columnas
            rows = cur.fetchall()  # Obtener todas las filas

            # Convertir filas a diccionarios
            return [dict(zip(columns, row)) for row in rows] if rows else None
    finally:
        conn.close()
