import boto3
import json
import os
import pip
import zipfile

def handler(event, context):

    packages = []
    packages.append('beautifulsoup4')
    packages.append('dnspython')
    packages.append('geoip2')
    packages.append('maxminddb')
    packages.append('netaddr')
    packages.append('pip')
    packages.append('requests')
    packages.append('smartopen')
    packages.append('whoisit')

    for package in packages:
        
        print('package: '+package)
        
        os.system('mkdir -p /tmp/'+package+'/python')
        if package == 'smartopen':
            os.system('pip install --target=/tmp/'+package+'/python/ smart_open[s3]')
        else:
            os.system('pip install --target=/tmp/'+package+'/python/ '+package)

        with zipfile.ZipFile('/tmp/'+package+'.zip', 'w') as zipf:
            for root, dirs, files in os.walk('/tmp/'+package+'/python/'):
                for file in files:
                    zipf.write(
                        os.path.join(root, file),
                        os.path.relpath(os.path.join(root, file),
                        os.path.join('/tmp', package))
                    )

    ### USE1 ###

        s3 = boto3.resource('s3', region_name = 'us-east-1')

        s3.meta.client.upload_file(
            '/tmp/'+package+'.zip',
            os.environ['USE1'],
            package+'.zip',
            ExtraArgs = {
                'ContentType': "application/zip"
            }
        )

    ### USE2 ###

        s3 = boto3.resource('s3', region_name = 'us-east-2')

        s3.meta.client.upload_file(
            '/tmp/'+package+'.zip',
            os.environ['USE2'],
            package+'.zip',
            ExtraArgs = {
                'ContentType': "application/zip"
            }
        )

    ### USW2 ###

        s3 = boto3.resource('s3', region_name = 'us-west-2')

        s3.meta.client.upload_file(
            '/tmp/'+package+'.zip',
            os.environ['USW2'],
            package+'.zip',
            ExtraArgs = {
                'ContentType': "application/zip"
            }
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Completed!')
    }
