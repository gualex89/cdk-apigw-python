import os
import json
import boto3
from db import fetch_solicitud


def handler(event, context):
    print(f"[START] Lambda execution started. RequestId={context.aws_request_id}")

    query_params = event.get("queryStringParameters", {}) or {}
    tipo_solicitud = query_params.get("tipo_solicitud")
    prioridad = query_params.get("prioridad")
    fecha_materializacion = query_params.get("fecha_materializacion")

    print(
        f"tipo_solicitud: {tipo_solicitud}, prioridad: {prioridad}, "
        f"fecha_materializacion: {fecha_materializacion}"
    )

    try:
        secret_name = os.environ["SECRET_NAME"]
        region_name = os.environ["AWS_REGION"]

        session = boto3.session.Session()
        client = session.client("secretsmanager", region_name=region_name)

        print("[INFO] Fetching database credentials from Secrets Manager...")
        secret_value = client.get_secret_value(SecretId=secret_name)
        creds = json.loads(secret_value["SecretString"])

        print(f"[INFO] Running query on host {creds['host']}...")
        result = fetch_solicitud(creds, tipo_solicitud, prioridad)

        print("[SUCCESS] Query executed successfully.")

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "ok": True,
                    "timestamp": str(result[0]) if result else None,
                    "tipo_solicitud": tipo_solicitud,
                    "prioridad": prioridad,
                    "fecha_materializacion": fecha_materializacion,
                    "result": list(result) if result else None,
                }
            ),
        }

    except Exception as e:
        print(f"[ERROR] Lambda failed: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"ok": False, "error": str(e)}),
        }
