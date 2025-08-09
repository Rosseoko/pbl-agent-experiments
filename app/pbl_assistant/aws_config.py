"""
AWS Configuration for Bedrock and other AWS services.
This file provides default configurations for AWS services when environment variables are not set.
"""
import os
import boto3
from botocore.config import Config

# Default AWS region if not specified in environment
DEFAULT_AWS_REGION = "us-east-1"

# Get AWS region from environment or use default
AWS_REGION = os.environ.get("AWS_REGION", DEFAULT_AWS_REGION)

# Set AWS_DEFAULT_REGION environment variable to ensure boto3 uses the correct region
os.environ["AWS_DEFAULT_REGION"] = AWS_REGION

# Create a default boto3 session with the region
def get_boto3_session():
    """
    Get a boto3 session with the configured region.
    """
    return boto3.Session(region_name=AWS_REGION)

# Create a bedrock runtime client with the configured region
def get_bedrock_client():
    """
    Get a bedrock runtime client with the configured region.
    """
    session = get_boto3_session()
    return session.client(
        'bedrock-runtime',
        config=Config(
            read_timeout=300,
            connect_timeout=300,
            retries={'max_attempts': 3}
        )
    )
