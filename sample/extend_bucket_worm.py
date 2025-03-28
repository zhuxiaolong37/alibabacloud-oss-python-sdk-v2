import argparse
import alibabacloud_oss_v2 as oss

parser = argparse.ArgumentParser(description="extend bucket worm sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--worm_id', help='The ID of the retention policy.', required=True)
parser.add_argument('--retention_period_in_days', help='The number of days for which objects can be retained.', required=True)


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

    result = client.extend_bucket_worm(oss.ExtendBucketWormRequest(
            bucket=args.bucket,
            worm_id=args.worm_id,
            extend_worm_configuration=oss.ExtendWormConfiguration(
                retention_period_in_days=args.retention_period_in_days,
            ),
    ))

    print(f'status code: {result.status_code},'
            f' request id: {result.request_id},'
    )


if __name__ == "__main__":
    main()