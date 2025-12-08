import os
import json
import boto3
from datetime import date, datetime
from decimal import Decimal
from helpers.db import fetch_solicitud


def json_serializer(obj):
    """Convierte dates y Decimals a string ISO o float"""
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)  # Convierte Decimal a float
    raise TypeError(f"Type {type(obj)} not serializable")


def handler(event, context):
    print(f"[START] Lambda execution started. RequestId={context.aws_request_id}")

    query_params = event.get("queryStringParameters", {}) or {}
    tipo_solicitud = query_params.get("tipo_solicitud")
    prioridad = query_params.get("prioridad")
    fecha_materializacion = query_params.get("fecha_materializacion")
    fecha_creacion_desde = query_params.get("fecha_creacion_desde")
    fecha_creacion_hasta = query_params.get("fecha_creacion_hasta")

    # Validar rangos de fecha de creación: o vienen ambos o ninguno
    if bool(fecha_creacion_desde) != bool(fecha_creacion_hasta):
        return {
            "statusCode": 400,
            "body": json.dumps({
                "ok": False,
                "error": "Debe enviar ambos parámetros fecha_creacion_desde y fecha_creacion_hasta si usa el filtro de fechas."
            }),
        }

    try:
        secret_name = os.environ["SECRET_NAME"]
        region_name = os.environ["AWS_REGION"]

        session = boto3.session.Session()
        client = session.client("secretsmanager", region_name=region_name)

        secret_value = client.get_secret_value(SecretId=secret_name)
        creds = json.loads(secret_value["SecretString"])

        result = fetch_solicitud(creds, tipo_solicitud, prioridad, fecha_materializacion, fecha_creacion_desde, fecha_creacion_hasta)

        return {
            "statusCode": 200,
            "body": json.dumps({"ok": True, "data": result}, default=json_serializer),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"ok": False, "error": str(e)}),
        }
