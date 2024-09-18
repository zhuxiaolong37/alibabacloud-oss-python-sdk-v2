import sys
import os
import argparse
import alibabacloud_oss_v2 as oss

# It is used only to execute sample code in the project directory
code_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(code_directory)

parser = argparse.ArgumentParser(description="list object versions sample")

parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')

def main():

    args = parser.parse_args()

    # Loading credentials values from the environment variables
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    # Using the SDK's default configuration
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    client = oss.Client(cfg)

    # Create the Paginator for the ListObjectVersions operation
    paginator = client.list_object_versions_paginator()

    # Iterate through the object version pages
    for page in paginator.iter_page(oss.ListObjectVersionsRequest(
            bucket=args.bucket
        )
    ):
        for o in page.version:
            print(f'Object version: {o.key}, {o.size}, {o.version_id} {o.last_modified}')

if __name__ == "__main__":
    main()
