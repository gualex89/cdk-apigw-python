#!/usr/bin/env python3
import aws_cdk as cdk
from aws_cdk import Environment
from mi_stage import MiStage

app = cdk.App()

# Cargar el contexto "dev" desde cdk.json o desde -c dev.xxx
env_context = app.node.try_get_context("dev") or app.node.get_context("dev")

if not isinstance(env_context, dict):
    raise ValueError("El contexto 'dev' no existe o no es válido.")

# Parámetros del entorno
account = env_context["account_id"]
region = env_context["region"]

primary_env = Environment(account=account, region=region)

# Crear el Stage DEV
MiStage(
    app,
    "DevStage",
    env=primary_env,
    env_name="dev",
    aws_vpc=env_context["aws_vpc"],
    aws_secret=env_context["aws_secret"],
    aws_arn_secret=env_context["aws_arn_secret"],
    aws_arn_db=env_context["aws_arn_db"],
)

app.synth()
