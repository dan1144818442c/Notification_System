from utils.mongo_client.connection import Connection
import gridfs
from utils.log.logger import Logger
from bson import ObjectId

logger = Logger.get_logger("MongoDAL_logger")

class DALError(Exception):
    """Base class for exceptions in this module."""
    pass

class MongoDAL:
    def __init__(self, connection: Connection):
        """Initialize with a MongoDB connection."""
        self.conn = connection
        self.db_conn = self.conn.connection
        self.fs = gridfs.GridFS(self.db_conn)

    def get_documents(self,collection_name, limit=None):
        """Returns the documents from MongoDB"""
        try:
            collection_conn = self.db_conn[collection_name]
            if limit is None:
                return [dict(doc) for doc in collection_conn.find({},{"_id":0})]
            return [dict(doc) for doc in collection_conn.find({},{"_id":0}).limit(limit)]
        except Exception as e:
            logger.error("Error retrieving documents")
            raise DALError(f"Error retrieving documents: {e}")


    def find_documents(self, collection_name, query):
        """Find a document in MongoDB based on a query"""
        try:
            collection_conn = self.db_conn[collection_name]
            return list(collection_conn.find(query))

        except Exception as e:
            logger.error("Error retrieving documents")
            raise DALError(f"Error retrieving documents with query {query}: {e}")


    def insert_document(self,collection_name, doc:dict):
        """Inserting a document into MongoDB"""
        try:
            collection_conn = self.db_conn[collection_name]
            collection_conn.insert_one(doc)
        except Exception as e:
            logger.error("Error inserting document")
            raise DALError(f"Error inserting document: {e}")

    def insert_binary(self,binary_data:bytes):
        """Inserting binary content into MongoDB"""
        try:
            file_id = self.fs.put(binary_data)
            return file_id
        except Exception as e:
            logger.error("Error inserting binary data into mongoDB")
            raise e

    def get_binary(self,file_id:str):
        """Returns binary content from MongoDB"""
        oid = ObjectId(file_id)
        try:
            b_data = self.fs.get(file_id=oid)
            return b_data.read()
        except Exception as e:
            logger.error("Error retrieving binary data from mongoDB")
            raise e
