from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_secretsmanager as secretsmanager,
    aws_apigateway as apigw,
    aws_cognito as cognito
)
from constructs import Construct


class MiStack(Stack):

    def __init__(self, scope: Construct, id: str, *,
                 env_name: str,
                 aws_secret: str,
                 **kwargs) -> None:

        super().__init__(scope, id, env=kwargs.get("env"))

        # 1️⃣ Secret
        secret = secretsmanager.Secret.from_secret_name_v2(
            self, f"{env_name}-rds-secret", aws_secret
        )

        # 2️⃣ Layer
        lambda_layer = _lambda.LayerVersion(
            self,
            f"{env_name}-deps-layer",
            code=_lambda.Code.from_asset("src/layers/deps"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12]
        )

        # 3️⃣ Lambda
        lambda_fn = _lambda.Function(
            self,
            f"{env_name}-lambda-rds",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.handler",
            code=_lambda.Code.from_asset("src/main"),
            timeout=Duration.seconds(20),
            memory_size=512,
            environment={
                "SECRET_NAME": aws_secret,
                "ENVIRONMENT": env_name
            },
            layers=[lambda_layer]
        )

        secret.grant_read(lambda_fn)

        # 4️⃣ API Gateway
        api = apigw.RestApi(
            self,
            f"{env_name}-api",
            rest_api_name=f"{env_name}-api"
        )

        validator = apigw.RequestValidator(
            self,
            f"{env_name}-validator",
            rest_api=api,
            validate_request_parameters=True
        )

        # 5️⃣ Cognito User Pool
        user_pool = cognito.UserPool(
            self,
            f"{env_name}-userpool-v2",
            self_sign_up_enabled=False,
            sign_in_aliases=cognito.SignInAliases(email=True),
        )

        # 6️⃣ Resource Server + Scope
        read_scope = cognito.ResourceServerScope(
            scope_name="read",
            scope_description="Read access"
        )

        resource_server = user_pool.add_resource_server(
            f"{env_name}-resource-server",
            identifier=f"{env_name.lower()}-api",
            scopes=[read_scope]
        )

        api_scope = cognito.OAuthScope.resource_server(
            resource_server, read_scope
        )

        # 7️⃣ Domain
        user_pool.add_domain(
            f"{env_name}-domain",
            cognito_domain=cognito.CognitoDomainOptions(
                domain_prefix=f"{env_name}-auth-v2-{id.lower()}"
            )
        )

        # 8️⃣ User Pool Client
        user_pool_client = user_pool.add_client(
            f"{env_name}-client",
            generate_secret=True,
            auth_flows=cognito.AuthFlow(
                user_password=False,
                admin_user_password=False
            ),
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(client_credentials=True),
                scopes=[api_scope]
            )
        )

        authorizer = apigw.CognitoUserPoolsAuthorizer(
            self,
            f"{env_name}-authorizer",
            cognito_user_pools=[user_pool]
        )

        # 🔟 Endpoints
        api.root.add_resource("health").add_method("GET")

        # Endpoint protegido
        db_test_resource = api.root.add_resource("db-test")

        db_test_resource.add_method(
            "GET",
            apigw.LambdaIntegration(lambda_fn),
            authorization_type=apigw.AuthorizationType.COGNITO,
            authorizer=authorizer,
            authorization_scopes=[f"{resource_server.user_pool_resource_server_id}/read"],
            request_parameters={
                "method.request.querystring.tipo_solicitud": True,
                "method.request.querystring.prioridad": True,
                "method.request.querystring.fecha_materializacion": False,
                "method.request.querystring.fecha_creacion_desde": False,
                "method.request.querystring.fecha_creacion_hasta": False
            },
            request_validator=validator
        )


        # Asignar el Authorizer al método manualmente
        
