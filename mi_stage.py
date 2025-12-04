from aws_cdk import Stage
from constructs import Construct
from mi_stack import MiStack

class MiStage(Stage):

    def __init__(self, scope: Construct, id: str, *, env_name: str,
                 aws_vpc: str, aws_secret: str, aws_arn_secret: str,
                 aws_arn_db: str, **kwargs) -> None:
        
        super().__init__(scope, id, **kwargs)

        # Guardar parámetros
        self.env_name = env_name
        self.aws_vpc = aws_vpc
        self.aws_secret = aws_secret
        self.aws_arn_secret = aws_arn_secret
        self.aws_arn_db = aws_arn_db

        # Crear el stack principal
        MiStack(
            self,
            f"{env_name.capitalize()}MainStack",
            env_name=env_name,
            aws_vpc=aws_vpc,
            aws_secret=aws_secret,
            aws_arn_secret=aws_arn_secret,
            aws_arn_db=aws_arn_db,
        )
