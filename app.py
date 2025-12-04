#!/usr/bin/env python3
import aws_cdk as cdk
from aws_cdk import Environment
from mi_stage import MiStage

app = cdk.App()

# Ambientes que queremos desplegar
ENVIRONMENTS = ["dev", "prod"]

for env_name in ENVIRONMENTS:
    # Obtener contexto desde cdk.json
    env_context = app.node.try_get_context(env_name)

    if not env_context:
        env_context = app.node.get_context(env_name)

    if not env_context:
        raise ValueError(f"Contexto para '{env_name}' no existe.")

    account = env_context["account_id"]
    region = env_context["region"]

    # Environment que CDK usará para desplegar
    primary_env = Environment(account=account, region=region)

    # Parámetros que pasaremos al Stage
    aws_vpc = env_context["aws_vpc"]
    aws_secret = env_context["aws_secret"]
    aws_arn_secret = env_context["aws_arn_secret"]
    aws_arn_db = env_context["aws_arn_db"]

    # Crear un Stage por ambiente (ej: DevStage, ProdStage)
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

