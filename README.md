# stacksets

This repository manages the distribution of Python Packages and CloudFormation StackSets used across the AWS Organization using **AWS CDK** for infrastructure as code.

## Features

- **Weekly curated Python Packages** packaged for Lambda Layers
- **Centralized S3 Distribution** across multiple AWS regions (us-east-1, us-east-2, us-west-2)
- **CloudFormation StackSets** with organization-wide SSM parameters
- **Automated deployment** using AWS CDK

------------------------------------------------------------------------

## Prerequisites

- **Python 3.9 or higher**
- **AWS CLI** configured with appropriate credentials
- **AWS CDK CLI** v2.x or higher
- AWS account with Organization enabled (for StackSets)
- IAM permissions to deploy CloudFormation stacks and create S3 buckets

------------------------------------------------------------------------

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jblukach/stacksets.git
   cd stacksets
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AWS credentials**
   ```bash
   aws configure
   ```

------------------------------------------------------------------------

## Project Structure

```
stacksets/
├── app.py                              # AWS CDK application entry point
├── cdk.json                            # CDK configuration and context
├── requirements.txt                    # Python dependencies
├── organization/
│   └── organization.py                 # Lambda function to fetch organization data
├── packages/
│   └── packages.py                     # Lambda function to package Python modules
└── stacksets/
    ├── __init__.py
    ├── stacksets_stack.py              # Base StackSet stack definition
    ├── stacksets_organization.py       # Organization StackSet
    ├── stacksets_packages.py           # Package distribution StackSet
    ├── stacksets_bucketuse1.py         # S3 bucket stack for us-east-1
    ├── stacksets_bucketuse2.py         # S3 bucket stack for us-east-2
    └── stacksets_bucketusw2.py         # S3 bucket stack for us-west-2
```

------------------------------------------------------------------------

## Deployment

### Synthesize CloudFormation Templates

Generate CloudFormation templates from CDK code:

```bash
cdk synth
```

### Deploy to AWS

Deploy the stacks to your AWS environment:

```bash
cdk deploy --all
```

To deploy a specific stack:

```bash
cdk deploy StackSetsBucketUse1
```

### List Available Stacks

View all available stacks in the app:

```bash
cdk list
```

------------------------------------------------------------------------

## Architecture

### System Overview

The project consists of three main components:

1. **S3 Regional Buckets** - Stores Lambda Layer packages in us-east-1, us-east-2, and us-west-2
2. **Package Distribution Service** - Lambda function that downloads, packages, and uploads Python packages weekly
3. **Organization Configuration Service** - Lambda function that maintains SSM parameters for organization and account information

### Workflow

1. **Package Generation** (Packages Lambda)
   - Downloads specified Python packages
   - Packages them in Lambda Layer format
   - Uploads to regional S3 buckets
   - Triggered weekly on Sunday at 11:00 AM UTC

2. **Organization Data Sync** (Organization Lambda)
   - Queries AWS Organization API
   - Generates CloudFormation template with SSM parameters
   - Uploads to S3
   - Triggered weekly on Sunday at 11:00 AM UTC

3. **StackSet Deployment**
   - CloudFormation StackSets deploy configurations to all organization accounts
   - Ensures consistent infrastructure and parameters across accounts

------------------------------------------------------------------------

## Overview

### Lambda Layer Package Distribution

Python Packages are **downloaded and packaged weekly** and published to Amazon S3 for use as **Lambda Layers** across the organization.

**Schedule** - Every Sunday at **11:00 AM UTC**

**Regions** - `us-east-1` - `us-east-2` - `us-west-2`

------------------------------------------------------------------------

## Included Python Packages

The following Python Packages are bundled for Lambda Layers:

- beautifulsoup4
- dnspython
- geoip2
- maxminddb
- netaddr
- pip
- requests
- smartopen
- whoisit

------------------------------------------------------------------------

## CloudFormation StackSets

CloudFormation templates are **generated weekly** and deployed using **AWS StackSets** to ensure consistent configuration across all accounts in the organization.

**Schedule** - Every Sunday at **11:00 AM UTC**

### StackSet Features

- Organization-wide deployment
- Centralized configuration using **AWS Systems Manager (SSM) Parameters**
- Automatic propagation to new accounts

### SSM Parameters

Each deployment creates and updates SSM Parameters containing:

- AWS Organization ID
- Account Numbers

These parameters are used by Lambda Functions and infrastructure components to dynamically reflect the organization structure and streamline IAM configuration.

------------------------------------------------------------------------

## Usage Examples

### Deploy the entire infrastructure

```bash
# First, synthesize to review CloudFormation templates
cdk synth

# Deploy all stacks
cdk deploy --all --require-approval=never
```

### Deploy a specific regional bucket

```bash
cdk deploy StackSetsBucketUse1 --require-approval=never
```

### View stack outputs

```bash
aws cloudformation describe-stacks --stack-name StackSetsBucketUse1 --query 'Stacks[0].Outputs'
```

### Destroy resources

```bash
# Destroy all stacks (will prompt for confirmation)
cdk destroy --all

# Destroy specific stack
cdk destroy StackSetsBucketUse1
```

------------------------------------------------------------------------

## Environment Variables

The Lambda functions expect the following environment variables to be configured through CloudFormation:

### Organization Lambda
- `S3_BUCKET` - S3 bucket name to upload organization configuration

### Packages Lambda
- `USE1` - S3 bucket in us-east-1 for package uploads
- `USE2` - S3 bucket in us-east-2 for package uploads
- `USW2` - S3 bucket in us-west-2 for package uploads

------------------------------------------------------------------------

## AWS CDK Commands

- `cdk list` - List all stacks
- `cdk synth` - Generate CloudFormation templates
- `cdk deploy` - Deploy stacks to AWS
- `cdk destroy` - Remove stacks from AWS
- `cdk diff` - Show differences between deployed and local state
- `cdk docs` - Open CDK documentation

------------------------------------------------------------------------

## Development

### Adding New Python Packages

Edit [packages/packages.py](packages/packages.py) and add the package name to the `packages` list:

```python
packages = []
packages.append('new-package-name')
```

### Adding New Regions

Create a new stack file in the [stacksets/](stacksets/) directory following the pattern of existing bucket stacks, then add it to [app.py](app.py).

### Local Testing

To test CDK code locally without deploying:

```bash
cdk synth
# Review the generated CloudFormation in cdk.out/
```

------------------------------------------------------------------------

## Troubleshooting

### Issue: "User is not authorized to perform: cloudformation:CreateStack"

**Solution**: Ensure your AWS IAM user has CloudFormation and related permissions. See [AWS CDK permissions documentation](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html#getting_started_prerequisites).

### Issue: "Organization not found"

**Solution**: Ensure your AWS account has AWS Organizations enabled and the IAM user has the necessary organization permissions.

### Issue: "Bucket already exists"

**Solution**: S3 bucket names must be globally unique. Check existing bucket names in [cdk.json](cdk.json) or modify the stack to use a unique bucket name.

------------------------------------------------------------------------

## License

See [LICENSE](LICENSE) file for details.

------------------------------------------------------------------------

## Support

For issues or questions, please open an issue on the repository.

