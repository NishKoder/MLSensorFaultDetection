import pymongo
import certifi
from typing import Any, Dict, List, Optional
import logging

import pymongo.collection
import pymongo.cursor
import pymongo.database
import pymongo.results

from utils.exceptions import AdvancedExceptionHandler
from utils.types import SimpleJson


MONGODB_URI = "your_mongodb_uri"
DATABASE_NAME = "your_database_name"

ca = certifi.where()


class MongoDBConnectionError(Exception):
    """Custom exception for MongoDB connection errors."""

    def __init__(self, message: str):
        """
        Initializes MongoDBConnectionError.

        Args:
            message (str): Error message.
        """
        self.message = message
        super().__init__(f"MongoDB connection error: {message}")


class MongoDBOperationError(Exception):
    """Custom exception for MongoDB operation errors."""

    def __init__(self, operation: str, message: str):
        """
        Initializes MongoDBOperationError.

        Args:
            operation (str): Operation being performed.
            message (str): Error message.
        """
        self.operation = operation
        self.message = message
        super().__init__(f"MongoDB operation error ({operation}): {message}")


class MongoDBClient:
    """
    A client for interacting with a MongoDB database.
    Provides methods for connecting to the database and performing CRUD operations.
    """

    client: Optional[pymongo.MongoClient] = None
    database: Optional[pymongo.database.Database] = None

    def __init__(
        self,
        uri: str = MONGODB_URI,
        database_name: str = DATABASE_NAME,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initializes the MongoDBClient and connects to the specified database.

        Args:
            uri (str): The MongoDB connection URI.
            database_name (str): The name of the database to connect to.
            logger (Optional[logging.Logger]): A logger instance for logging.
                If None, a default logger is created.

        Raises:
            MongoDBConnectionError: If there is an error connecting to the database.
        """
        self.exception_handler = AdvancedExceptionHandler(logger=logger)
        try:
            self.client = pymongo.MongoClient(uri, tlsCAFile=ca)
            self.database = self.client[database_name]
            self.exception_handler.logger.info(
                f"Connected to MongoDB database: {database_name}"
            )
        except Exception as e:
            self.exception_handler.handle_exception(
                e, "Failed to connect to MongoDB."
            )
            raise MongoDBConnectionError(str(e))

    def get_collection(self, collection_name: str) -> pymongo.collection.Collection:
        """
        Gets a specified collection from the database.

        Args:
            collection_name (str): The name of the collection to retrieve.

        Returns:
            pymongo.collection.Collection: The requested collection.

        Raises:
            MongoDBOperationError: If there is an error retrieving the collection.
        """
        self.exception_handler.validate_input(collection_name, str, "collection_name")
        if not self.database:
            self.exception_handler.handle_exception(
                MongoDBConnectionError("Not connected to a database.")
            )
            raise MongoDBConnectionError("Not connected to a database.")

        try:
            return self.database[collection_name]
        except Exception as e:
            self.exception_handler.handle_exception(
                e, f"Failed to get collection: {collection_name}"
            )
            raise MongoDBOperationError("get_collection", str(e))

    def insert_document(
        self,
        collection_name: str,
        document: SimpleJson,
    ) -> Any:
        """
        Inserts a single document into the specified collection.

        Args:
            collection_name (str): The name of the collection.
            document (Dict[str, Any]): The document to insert.

        Returns:
            Any: The ID of the inserted document.

        Raises:
            MongoDBOperationError: If there is an error inserting the document.
        """
        self.exception_handler.validate_input(collection_name, str, "collection_name")
        self.exception_handler.validate_input(document, dict, "document")
        try:
            collection: pymongo.collection.Collection = self.get_collection(
                collection_name
            )
            result: pymongo.results.InsertOneResult = collection.insert_one(document)
            return result.inserted_id
        except Exception as e:
            self.exception_handler.handle_exception(
                e, f"Failed to insert document into {collection_name}"
            )
            raise MongoDBOperationError("insert_document", str(e))

    def find_documents(
        self,
        collection_name: str,
        query: SimpleJson,
    ) -> List[Dict[str, Any]]:
        """
        Finds documents in the specified collection that match the given query.

        Args:
            collection_name (str): The name of the collection.
            query (Dict[str, Any]): The query to filter documents.

        Returns:
            List[Dict[str, Any]]: A list of documents that match the query.

        Raises:
            MongoDBOperationError: If there is an error finding the documents.
        """
        self.exception_handler.validate_input(collection_name, str, "collection_name")
        self.exception_handler.validate_input(query, dict, "query")
        try:
            collection: pymongo.collection.Collection = self.get_collection(
                collection_name
            )
            cursor: pymongo.cursor.Cursor = collection.find(query)
            return list(cursor)
        except Exception as e:
            self.exception_handler.handle_exception(
                e, f"Failed to find documents in {collection_name}"
            )
            raise MongoDBOperationError("find_documents", str(e))

    def update_document(
        self,
        collection_name: str,
        query: SimpleJson,
        update_values: SimpleJson,
    ) -> int:
        """
        Updates a single document in the specified collection that matches the given query.

        Args:
            collection_name (str): The name of the collection.
            query (Dict[str, Any]): The query to find the document to update.
            update_values (Dict[str, Any]): The new values to update the document with.

        Returns:
            int: The number of documents modified.

        Raises:
            MongoDBOperationError: If there is an error updating the document.
        """
        self.exception_handler.validate_input(collection_name, str, "collection_name")
        self.exception_handler.validate_input(query, dict, "query")
        self.exception_handler.validate_input(update_values, dict, "update_values")

        try:
            collection: pymongo.collection.Collection = self.get_collection(
                collection_name
            )
            result: pymongo.results.UpdateResult = collection.update_one(
                query, {"$set": update_values}
            )
            return result.modified_count
        except Exception as e:
            self.exception_handler.handle_exception(
                e, f"Failed to update document in {collection_name}"
            )
            raise MongoDBOperationError("update_document", str(e))

    def delete_document(self, collection_name: str, query: SimpleJson) -> int:
        """
        Deletes a single document in the specified collection that matches the given query.

        Args:
            collection_name (str): The name of the collection.
            query (Dict[str, Any]): The query to find the document to delete.

        Returns:
            int: The number of documents deleted.

        Raises:
            MongoDBOperationError: If there is an error deleting the document.
        """
        self.exception_handler.validate_input(collection_name, str, "collection_name")
        self.exception_handler.validate_input(query, dict, "query")

        try:
            collection: pymongo.collection.Collection = self.get_collection(
                collection_name
            )
            result: pymongo.results.DeleteResult = collection.delete_one(query)
            return result.deleted_count
        except Exception as e:
            self.exception_handler.handle_exception(
                e, f"Failed to delete document in {collection_name}"
            )
            raise MongoDBOperationError("delete_document", str(e))
