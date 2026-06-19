import boto3
import json
import os
import shutil
import subprocess
import zipfile

def handler(event, context):

    # Include common Lambda layer binary locations so layer-provided CLIs are discoverable.
    os.environ['PATH'] = '/opt/bin:/opt/python/bin:' + os.environ.get('PATH', '')
    os.environ['UV_CACHE_DIR'] = '/tmp/uv-cache'
    os.environ['UV_PYTHON_DOWNLOADS'] = 'never'

    packages = []
    packages.append('beautifulsoup4')
    packages.append('dnspython')
    packages.append('fastmcp')
    packages.append('geoip2')
    packages.append('mangum')
    packages.append('maxminddb')
    packages.append('netaddr')
    packages.append('redis')
    packages.append('requests')
    packages.append('smartopen')
    packages.append('uv')
    packages.append('whoisit')

    uv_executable = shutil.which('uv')
    if not uv_executable:
        raise RuntimeError('uv binary not found in Lambda layer. Expected in /opt/bin or /opt/python/bin.')

    print('uv executable: '+uv_executable)
    uv_version = subprocess.run([uv_executable, '--version'], check=True, capture_output=True, text=True)
    print('uv version: '+uv_version.stdout.strip())

    for package in packages:
        
        print('package: '+package)
        
        os.system('mkdir -p /tmp/'+package+'/python')
        install_target = '/tmp/'+package+'/python/'

        if package == 'smartopen':
            install_package = 'smart_open[s3]'
        else:
            install_package = package

        print('installer: uv (package: '+install_package+')')
        command = [
            uv_executable,
            'pip',
            'install',
            '--python',
            '/var/lang/bin/python3.13',
            '--target',
            install_target,
            install_package
        ]

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as err:
            print('uv command failed: '+' '.join(command))
            if err.stdout:
                print('uv stdout:\n'+err.stdout)
            if err.stderr:
                print('uv stderr:\n'+err.stderr)
            raise

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
