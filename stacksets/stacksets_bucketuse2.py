from aws_cdk import (
    RemovalPolicy,
    Stack,
    aws_iam as _iam,
    aws_s3 as _s3,
    aws_ssm as _ssm
)

from constructs import Construct

class StackSetsBucketUse2(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

    ### PARAMETER ###

        organization = _ssm.StringParameter.from_string_parameter_attributes(
            self, 'organization',
            parameter_name = '/organization/id'
        )

    ### BUCKET ###

        bucket = _s3.Bucket(
            self, 'bucket',
            bucket_name = 'packages-use2-lukach-io',
            encryption = _s3.BucketEncryption.S3_MANAGED,
            block_public_access = _s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy = RemovalPolicy.DESTROY,
            auto_delete_objects = True,
            enforce_ssl = True,
            versioned = False
        )

        bucket_policy = _iam.PolicyStatement(
            effect = _iam.Effect(
                'ALLOW'
            ),
            principals = [
                _iam.AnyPrincipal()
            ],
            actions = [
                's3:ListBucket'
            ],
            resources = [
                bucket.bucket_arn
            ],
            conditions = {"StringEquals": {"aws:PrincipalOrgID": organization.string_value}}
        )

        bucket.add_to_resource_policy(bucket_policy)

        object_policy = _iam.PolicyStatement(
            effect = _iam.Effect(
                'ALLOW'
            ),
            principals = [
                _iam.AnyPrincipal()
            ],
            actions = [
                's3:GetObject'
            ],
            resources = [
                bucket.arn_for_objects('*')
            ],
            conditions = {"StringEquals": {"aws:PrincipalOrgID": organization.string_value}}
        )

        bucket.add_to_resource_policy(object_policy)
