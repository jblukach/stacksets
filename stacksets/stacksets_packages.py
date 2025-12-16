import datetime

from aws_cdk import (
    Duration,
    RemovalPolicy,
    Size,
    Stack,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_logs as _logs,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_s3 as _s3
)

from constructs import Construct

class StacksetsPackages(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        year = datetime.datetime.now().strftime('%Y')
        month = datetime.datetime.now().strftime('%m')

    ### S3 BUCKET ###

        bucket = _s3.Bucket.from_bucket_name(
            self, 'bucket',
            bucket_name = 'stacksets-deployment-lukach-io'
        )
    
    ### LAMBDA LAYER ###

        pip = _lambda.LayerVersion(
            self, 'pip',
            layer_version_name = 'pip',
            description = str(year)+'-'+str(month),
            code = _lambda.Code.from_bucket(
                bucket = bucket,
                key = 'pip.zip'
            ),
            compatible_architectures = [
                _lambda.Architecture.ARM_64
            ],
            compatible_runtimes = [
                _lambda.Runtime.PYTHON_3_13
            ],
            removal_policy = RemovalPolicy.DESTROY
        )

    ### IAM ROLE ###

        role = _iam.Role(
            self, 'role', 
            assumed_by = _iam.ServicePrincipal(
                'lambda.amazonaws.com'
            )
        )

        role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                'service-role/AWSLambdaBasicExecutionRole'
            )
        )

        role.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    's3:PutObject'
                ],
                resources = [
                    bucket.arn_for_objects('*')
                ]
            )
        )

    ### LAMBDA ###

        packages = _lambda.Function(
            self, 'packages',
            runtime = _lambda.Runtime.PYTHON_3_13,
            architecture = _lambda.Architecture.ARM_64,
            code = _lambda.Code.from_asset('packages'),
            handler = 'packages.handler',
            environment = dict(
                S3_BUCKET = bucket.bucket_name
            ),
            ephemeral_storage_size = Size.gibibytes(1),
            timeout = Duration.seconds(900),
            memory_size = 2048,
            role = role,
            layers = [
                pip
            ]
        )

        logs = _logs.LogGroup(
            self, 'logs',
            log_group_name = '/aws/lambda/'+packages.function_name,
            retention = _logs.RetentionDays.ONE_WEEK,
            removal_policy = RemovalPolicy.DESTROY
        )

        event = _events.Rule(
            self, 'event',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '11',
                month = '*',
                week_day = 'SUN',
                year = '*'
            )
        )

        event.add_target(
            _targets.LambdaFunction(packages)
        )
