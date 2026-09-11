import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.vectors as oss_vectors

parser = argparse.ArgumentParser(description="vector put vector index fusion sample")
parser.add_argument('--region', help='The region in which the bucket is located.', required=True)
parser.add_argument('--bucket', help='The name of the bucket.', required=True)
parser.add_argument('--endpoint', help='The domain names that other services can use to access OSS')
parser.add_argument('--index_name', help='The name of the fusion vector index.', required=True)
parser.add_argument('--account_id', help='The account id.', required=True)

def main():
    args = parser.parse_args()

    # Loading credentials values from the environment variables
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    # Using the SDK's default configuration
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider
    cfg.region = args.region
    cfg.account_id = args.account_id
    if args.endpoint is not None:
        cfg.endpoint = args.endpoint

    vector_client = oss_vectors.Client(cfg)

    # A fusion index is described by a schema listing every field, instead of
    # the single vector field that put_vector_index configures. Two vector
    # fields are allowed, which is what makes a fusion index different from a
    # standard one.
    #
    # The schema is a plain dict, so any field type or property the service
    # supports travels through unchanged. Write a boolean out explicitly when
    # false is what you mean, an omitted property and a property set to false
    # are not the same thing to the service.
    schema_configuration = {
        "fields": [
            {
                "name": "text_vector",
                "type": "vector",
                "dataType": "float32",
                "dimension": 4,
                "distanceMetric": "cosine"
            },
            {
                "name": "image_vector",
                "type": "vector",
                "dataType": "float32",
                "dimension": 4,
                "distanceMetric": "cosine"
            },
            {
                "name": "title",
                "type": "text",
                "exactMatch": False,
                "text": {
                    "enabled": True,
                    "analyzer": "single_word",
                    "analyzerParameters": {
                        "caseSensitive": False,
                        "delimitWord": False,
                        "delimiter": ""
                    }
                }
            }
        ]
    }

    result = vector_client.put_vector_index_fusion(oss_vectors.models.PutVectorIndexFusionRequest(
        bucket=args.bucket,
        index_name=args.index_name,
        schema_configuration=schema_configuration
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
    )

if __name__ == "__main__":
    main()
