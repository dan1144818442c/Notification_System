from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from log.logger import Logger

logger = Logger.get_logger("ElasticDAL_logger")



class ElasticDAL:
    """Data Access Layer for Elasticsearch operations."""

    def __init__(self, es_client: Elasticsearch, index_name: str, mapping: dict = None):
        self.es_client = es_client
        self.index_name = index_name
        if mapping is not None:
            self.mapping = mapping
        else:
            self.mapping = ElasticDAL._get_mapping()
        self._create_index()

    def _create_index(self):
        """Create the Elasticsearch index if it doesn't exist."""
        if not self.es_client.indices.exists(index=self.index_name):
            self.es_client.indices.create(index=self.index_name, mappings=self.mapping)
            logger.info(f"Index '{self.index_name}' created.")
        else:
            logger.info(f"Index '{self.index_name}' already exists.")

    @staticmethod
    def _get_mapping():
        """Define the mapping for the Elasticsearch index."""
        logger.info("Define the mapping for the Elasticsearch index.")
        return {
            "properties":{

            }
        }

    def create_documents(self, documents:list):
        """Bulk insert documents into the Elasticsearch index."""
        actions = [
            {
                "_index": self.index_name,
                "_id": doc["file_id"],
                "_source": doc
            }
            for doc in documents
        ]
        try:
            response = bulk(self.es_client, actions, stats_only=True)
            logger.info("The documents were successfully saved to MongoDB.")
            return response
        except Exception as e:
            logger.error("Error in bulk insert")
            raise Exception(f"Error in bulk insert: {e}")

    def get_documents(self,size: int = 100):
        """Retrieve documents from the Elasticsearch index."""
        try:
            response = self.es_client.search(index=self.index_name, body={"query": {"match_all": {}}}, size=size)
            logger.info("The documents were successfully Retrieve from MongoDB.")
            return [{"_id": hit["_id"],
                     **hit["_source"]}
                    for hit in
                    response["hits"]["hits"]]
        except Exception as e:
            raise Exception(f"Error searching documents: {e}")

    def update_documents(self, updates:list, name_id: str = "id"):
        """Bulk update documents in the Elasticsearch index."""
        actions = [
            {
                "_op_type": "update",
                "_index": self.index_name,
                "_id": doc[name_id],
                "doc":  {
                    k: v for k, v in doc.items() if k != "_id"
                }
            }
            for doc in updates
        ]
        try:
            response = bulk(self.es_client, actions, stats_only=False)
            return response
        except Exception as e:
            raise Exception(f"Error in bulk update: {e}")