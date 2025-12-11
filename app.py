#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacksets.stacksets_stack import StacksetsStack

app = cdk.App()

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