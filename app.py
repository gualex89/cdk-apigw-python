#!/usr/bin/env python3
import aws_cdk as cdk
from aws_cdk import Environment
from mi_stage import MiStage

app = cdk.App()

# ❗ Ambiente fijo (DEV) — sin context
account = "798429904238"
region = "us-east-2"

aws_vpc = "vpc-05d1bf6aa6b689c5b"
aws_secret = "test2/rds-credentials"
aws_arn_secret = "arn:aws:secretsmanager:us-east-2:798429904238:secret:test2/rds-credentials-a4cykn"
aws_arn_db = "arn:aws:rds:us-east-2:798429904238:db:datos-clientes"

primary_env = Environment(account=account, region=region)

MiStage(
    app,
    "DevStage",
    env=primary_env,
    env_name="dev",
    aws_vpc=aws_vpc,
    aws_secret=aws_secret,
    aws_arn_secret=aws_arn_secret,
    aws_arn_db=aws_arn_db,
)

app.synth()
