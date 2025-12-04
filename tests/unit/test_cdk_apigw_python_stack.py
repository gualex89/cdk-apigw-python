import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_apigw_python.cdk_apigw_python_stack import CdkApigwPythonStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_apigw_python/cdk_apigw_python_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkApigwPythonStack(app, "cdk-apigw-python")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
