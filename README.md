# stacksets

This repository manages the distribution of Python Packages and CloudFormation StackSets used across the AWS Organization.

It provides: - Weekly curated Python Packages packaged for **Lambda Layers** - centralized **S3 Distribution** across multiple AWS regions - **CloudFormation StackSets** with organization-wide SSM parameters.

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
- ip2Location
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
