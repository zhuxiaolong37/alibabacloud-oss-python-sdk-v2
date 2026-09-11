import argparse
import alibabacloud_oss_v2 as oss
import alibabacloud_oss_v2.vectors as oss_vectors

parser = argparse.ArgumentParser(description="vector query vectors fusion sample")
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

    # QueryVectorsFusion accepts three shapes of query, and they can be mixed:
    #
    #   knn        a single dict for one nearest neighbour clause, or a list of
    #              dicts for several of them. Both encode correctly, an object
    #              and an array on the wire.
    #   query      a scalar or full text expression. The field names and the
    #              operator names are dynamic, so this stays a plain dict.
    #   retriever  a tree that combines several retrievers into one ranked
    #              result, for example an rrf node holding knn and text
    #              components.
    #
    # Every hit of the result carries a score. That score belongs to this
    # operation only, the standard QueryVectors result keeps reporting
    # distance and the two are never mixed.
    result = vector_client.query_vectors_fusion(oss_vectors.models.QueryVectorsFusionRequest(
        bucket=args.bucket,
        index_name=args.index_name,
        knn={
            "field": "text_vector",
            "queryVector": [0.1] * 4,
            "topK": 10,
            "numCandidates": 100
        },
        query={
            "$and": [{
                "title": {
                    "$textMatch": "cloud storage"
                }
            }]
        },
        return_metadata=True,
        sort=[{
            "score": {
                "order": "desc"
            }
        }],
        limit=10
    ))

    print(f'status code: {result.status_code},'
          f' request id: {result.request_id},'
          f' next token: {result.next_token},'
          )

    if result.vectors:
        for vector in result.vectors:
            print(f'vector: {vector}')


if __name__ == "__main__":
    main()
