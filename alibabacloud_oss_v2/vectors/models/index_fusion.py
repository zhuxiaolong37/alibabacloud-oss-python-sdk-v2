from typing import Optional, Any, Dict
from ... import serde


class PutVectorIndexFusionRequest(serde.RequestModel):
    """
    The request for the PutVectorIndexFusion operation.

    Creates a fusion index. A fusion index is described by a schema covering
    every field of the index, instead of the single vector field that
    PutVectorIndex configures.

    The schema is a plain dict rather than a typed model on purpose:

    - serde.Model silently drops every constructor keyword argument that is
      not listed in _attribute_map, so a typed schema would not report a
      misspelled property, it would just send a smaller schema and let the
      service complain about a missing field instead.
    - the JSON serializer of this module hands body values straight to
      json.dumps, which cannot encode a nested Model.
    - a dict also carries properties a future service version adds, without
      waiting for an SDK release.

    The wire format looks like this::

        {
            "fields": [
                {
                    "name": "text_vector",
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

    Write booleans out explicitly whenever false is what you mean. An omitted
    property and a property set to false are not the same thing to the
    service, so exactMatch=false and text.enabled=false both have to appear in
    the dict to take effect.
    """

    _attribute_map = {
        'bucket': {'tag': 'input', 'position': 'host', 'rename': 'bucket', 'type': 'str', 'required': True},
        'index_name': {'tag': 'input', 'position': 'body', 'rename': 'indexName', 'type': 'str', 'required': True},
        'mode': {'tag': 'input', 'position': 'body', 'rename': 'mode', 'type': 'str'},
        'schema_configuration': {'tag': 'input', 'position': 'body', 'rename': 'schemaConfiguration', 'type': 'dict', 'required': True},
    }

    def __init__(
        self,
        bucket: str = None,
        index_name: Optional[str] = None,
        mode: Optional[str] = None,
        schema_configuration: Optional[Dict] = None,
        **kwargs: Any
    ) -> None:
        """
        Args:
            bucket (str, required): The name of the bucket.
            index_name (str, required): The name of the fusion index.
            mode (str, optional): The mode of the index.
            schema_configuration (Dict, required): The schema of the fusion
                index, a dict holding a "fields" list. See the class
                docstring for the shape of every field entry.
        """
        super().__init__(**kwargs)
        self.bucket = bucket
        self.index_name = index_name
        self.mode = mode
        self.schema_configuration = schema_configuration


class PutVectorIndexFusionResult(serde.ResultModel):
    """
    The result for the PutVectorIndexFusion operation.
    """
