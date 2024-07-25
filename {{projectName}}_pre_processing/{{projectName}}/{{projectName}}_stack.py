from aws_cdk import (
    Size,
    Duration,
    Stack,
    aws_s3 as s3,
    aws_dynamodb as db,
    aws_lambda as _lambda,
    RemovalPolicy
)
from constructs import Construct


class {{stack_projectName}}Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DEFINE SOURCE BUCKET
        # Assuming that the bucket already exists

        SOURCE_BUCKET = "<PUT BUCKET NAME HERE>"

        source_s3_bucket = s3.Bucket.from_bucket_arn(
            self,
            SOURCE_BUCKET,
            f'arn:aws:s3:::{SOURCE_BUCKET.lower()}'
        )

        target_s3_bucket = s3.Bucket(
            self,
            f"{SOURCE_BUCKET}-destination",
            # Change the removal_policy to RemovalPolicy.RETAIN when ready for production
            # Above comment is very important
            removal_policy=RemovalPolicy.DESTROY
        )

        metadata = db.Table(
            self,
            f'{SOURCE_BUCKET.capitalize()}-MetaData',
            partition_key=db.Attribute(
                name='FilePath', type=db.AttributeType.STRING
            ),
            billing_mode=db.BillingMode.PAY_PER_REQUEST,
            # Change the removal_policy to RemovalPolicy.RETAIN when ready for production
            # Above comment is very important
            removal_policy=RemovalPolicy.DESTROY
        )

        # docker based lambda function
        lambda_with_docker = _lambda.DockerImageFunction(
            self,
            f'{SOURCE_BUCKET.capitalize()}-Lambda-ChangeMe',
            code=_lambda.DockerImageCode.from_image_asset(
                directory='lambda/first_step'
            ),
            environment={
                'SOURCE_BUCKET': source_s3_bucket.bucket_name,
                'TARGET_BUCKET': target_s3_bucket.bucket_name,
                'METADATA': metadata.table_name
            },
            ephemeral_storage_size=Size.gibibytes(2),
            timeout=Duration.minutes(5),
            memory_size=128
        )

        # lambda code direct - no package installation required
        stop_lambda = _lambda.Function(
            self, "StopInstanceLambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="stop_instance.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                'SOURCE_BUCKET': source_s3_bucket.bucket_name,
                'TARGET_BUCKET': target_s3_bucket.bucket_name,
                'METADATA': metadata.table_name
            }
        )

        source_s3_bucket.grant_read(lambda_with_docker)
        target_s3_bucket.grant_read_write(lambda_with_docker)
        metadata.grant_read_write_data(lambda_with_docker)
