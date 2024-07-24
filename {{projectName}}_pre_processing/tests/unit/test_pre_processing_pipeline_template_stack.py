import aws_cdk as core
import aws_cdk.assertions as assertions

from pre_processing_pipeline_template.pre_processing_pipeline_template_stack import PreProcessingPipelineTemplateStack

# example tests. To run these tests, uncomment this file along with the example
# resource in pre_processing_pipeline_template/pre_processing_pipeline_template_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = PreProcessingPipelineTemplateStack(app, "pre-processing-pipeline-template")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
