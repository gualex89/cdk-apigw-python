#!/usr/bin/env python3
import aws_cdk as cdk
from aws_cdk import Environment
from mi_stage import MiStage

app = cdk.App()

# Ambientes que queremos desplegar
ENVIRONMENTS = ["dev", "prod"]

for env_name in ENVIRONMENTS:
    
    # Obtener contexto desde la CLI (-c dev) o desde cdk.json
    env_context = app.node.try_get_context(env_name)

    # Si el contexto viene como True (cuando usamos -c dev), cargar el bloque real desde cdk.json
    if env_context is True:
        env_context = app.node.get_context(env_name)

    # Si sigue sin haber contexto, error
    if not isinstance(env_context, dict):
        raise ValueError(f"Contexto para '{env_name}' no existe o no es válido.")

    # Extraer valores del contexto
    account = env_context["account_id"]
    region = env_context["region"]

    primary_env = Environment(account=account, region=region)

    aws_vpc = env_context["aws_vpc"]
    aws_secret = env_context["aws_secret"]
    aws_arn_secret = env_context["aws_arn_secret"]
    aws_arn_db = env_context["aws_arn_db"]

    MiStage(
        app,
        f"{env_name.capitalize()}Stage",
        env=primary_env,
        env_name=env_name,
        aws_vpc=aws_vpc,
        aws_secret=aws_secret,
        aws_arn_secret=aws_arn_secret,
        aws_arn_db=aws_arn_db,
    )

app.synth()
