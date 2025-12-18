# stacksets

This repository manages the distribution of Python packages and CloudFormation StackSets used across the AWS Organization.

It provides: - Weekly curated Python packages packaged for **Lambda Layers** - centralized **S3 Distribution** across multiple AWS regions - **CloudFormation StackSets** with organization-wide SSM parameters.

------------------------------------------------------------------------

## Overview

### Lambda Layer Package Distribution

Python packages are **downloaded and packaged weekly** and published to Amazon S3 for use as **shared Lambda Layers** across the organization.

**Schedule** - Every Sunday at **11:00 AM UTC**

**Regions** - `us-east-1` - `us-east-2` - `us-west-2`

These packages are intended to be referenced by Lambda functions without duplicating dependencies per account.

------------------------------------------------------------------------

## Included Python Packages

The following Python packages are bundled for Lambda Layers:

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

These parameters are consumed by Lambda functions and other infrastructure components to dynamically adapt to the organization structure.

------------------------------------------------------------------------
