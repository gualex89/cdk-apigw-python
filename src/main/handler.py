import os
import json
import boto3
import psycopg2


def handler(event, context):
    # 1️⃣ Log de inicio
    print(f"[START] Lambda execution started. RequestId={context.aws_request_id}")
    
    tipo_solicitud = event.get('queryStringParameters', {}).get('tipo_solicitud')
    prioridad = event.get('queryStringParameters', {}).get('prioridad')
    fecha_materializacion = event.get('queryStringParameters', {}).get('fecha_materializacion')

    print(f"tipo_solicitud: {tipo_solicitud}, prioridad: {prioridad}, fecha_materializacion: {fecha_materializacion}")
    
    try:
        # Leer variables de entorno
        secret_name = os.environ["SECRET_NAME"]
        region_name = os.environ["AWS_REGION"]

        # Obtener credenciales desde Secrets Manager
        session = boto3.session.Session()
        client = session.client("secretsmanager", region_name=region_name)

        print("[INFO] Fetching database credentials from Secrets Manager...")
        secret_value = client.get_secret_value(SecretId=secret_name)
        creds = json.loads(secret_value["SecretString"])

        # 2️⃣ Log de intento de conexión
        print(f"[INFO] Connecting to database host: {creds['host']}...")

        conn = psycopg2.connect(
            host=creds["host"],
            database=creds["dbname"],
            user=creds["username"],
            password=creds["password"],
            port=creds["port"]
        )

        cur = conn.cursor()
        cur.execute("SELECT * from solicitudes WHERE tipo_solicitud = %s AND prioridad = %s;", (tipo_solicitud, prioridad))
        result = cur.fetchone()

        cur.close()
        conn.close()

        # 3️⃣ Log final de éxito
        print("[SUCCESS] Query executed successfully.")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "ok": True,
                "timestamp": str(result[0]),
                "tipo_solicitud": tipo_solicitud,
                "prioridad": prioridad,
                "fecha_materializacion": fecha_materializacion
            })
        }

    except Exception as e:
        # 3️⃣ Log final de error
        print(f"[ERROR] Lambda failed: {str(e)}")

        return {
            "statusCode": 500,
            "body": json.dumps({
                "ok": False,
                "error": str(e)
            })
        }
