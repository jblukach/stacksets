#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacksets.stacksets_bucketuse1 import StackSetsBucketUse1
from stacksets.stacksets_bucketuse2 import StackSetsBucketUse2
from stacksets.stacksets_bucketusw2 import StackSetsBucketUsw2
from stacksets.stacksets_organization import StacksetsOrganization
from stacksets.stacksets_packages import StacksetsPackages
from stacksets.stacksets_stack import StacksetsStack

app = cdk.App()

StackSetsBucketUse1(
    app, 'StackSetsBucketUse1',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-1'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

StackSetsBucketUse2(
    app, 'StackSetsBucketUse2',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

StackSetsBucketUsw2(
    app, 'StackSetsBucketUsw2',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-west-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

StacksetsOrganization(
    app, 'StacksetsOrganization',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

StacksetsPackages(
    app, 'StacksetsPackages',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

StacksetsStack(
    app, 'StacksetsStack',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

cdk.Tags.of(app).add('Alias','stacksets')
cdk.Tags.of(app).add('GitHub','https://github.com/jblukach/stacksets')
cdk.Tags.of(app).add('Org','lukach.io')

app.synth()