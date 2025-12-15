import boto3
import json
import os

def handler(event, context):

    client = boto3.client('organizations')

    organization = client.describe_organization()

    f = open('/tmp/organization.yaml', 'w')

    f.write('AWSTemplateFormatVersion: 2010-09-09\n')
    f.write('Description: Organization & Accounts Parameters\n')
    f.write('Resources:\n')
    f.write('  organization:\n')
    f.write('    Type: AWS::SSM::Parameter\n')
    f.write('    Properties:\n')
    f.write('      Name: /organization/id\n')
    f.write('      Type: String\n')
    f.write('      Value: '+ organization['Organization']['Id']+'\n')
    f.write('      Tier: Standard\n')

    paginator = client.get_paginator('list_accounts')
    page_iterator = paginator.paginate()
    accounts = []
    for page in page_iterator:
        accounts.extend(page['Accounts'])
    for account in accounts:
        f.write('  '+account['Name']+':\n')
        f.write('    Type: AWS::SSM::Parameter\n')
        f.write('    Properties:\n')
        f.write('      Name: /account/'+account['Name']+'\n')
        f.write('      Type: String\n')
        f.write('      Value: '+account['Id']+'\n')
        f.write('      Tier: Standard\n')

    f.close()

    client = boto3.client('s3')
    client.upload_file('/tmp/organization.yaml', os.environ['S3_BUCKET'], 'organization.yaml')

    return {
        'statusCode': 200,
        'body': json.dumps('Completed!')
    }