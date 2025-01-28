import logging
import unittest
from unittest.mock import patch, MagicMock

import certifi

from AIUtiils.db_connectors import (
    MongoDBClient,
    MongoDBConnectionError,
    MongoDBOperationError,
)

ca = certifi.where()

class TestMongoDBClient(unittest.TestCase):
    """
    Test suite for the MongoDBClient class.
    """

    @patch("pymongo.MongoClient")
    def setUp(self, mock_mongo_client: MagicMock):
        """
        Sets up a test instance of MongoDBClient with a mocked MongoClient.
        """
        self.mock_mongo_client = mock_mongo_client
        self.test_db_name = "test_db"
        self.test_collection_name = "test_collection"

        # Mock the return value of pymongo.MongoClient
        self.mock_client_instance = MagicMock()
        self.mock_mongo_client.return_value = self.mock_client_instance

        # Mock the database
        self.mock_db = MagicMock()
        self.mock_client_instance.__getitem__.return_value = self.mock_db

        # Mock the collection
        self.mock_collection = MagicMock()
        self.mock_db.__getitem__.return_value = self.mock_collection

        self.client = MongoDBClient(
            uri="mock_uri",
            database_name=self.test_db_name,
            logger=logging.getLogger("test_logger")
        )

    def test_connection_success(self):
        """
        Tests that the MongoDB client establishes a connection successfully.
        """
        self.mock_mongo_client.assert_called_once_with("mock_uri", tlsCAFile=ca)
        self.mock_client_instance.__getitem__.assert_called_with(self.test_db_name)
        self.assertIsNotNone(self.client.client)
        self.assertIsNotNone(self.client.database)

    @patch("pymongo.MongoClient")
    def test_connection_failure(self, mock_mongo_client: MagicMock):
        """
        Tests that the MongoDB client raises a MongoDBConnectionError 
        on connection failure.
        """
        mock_mongo_client.side_effect = Exception("Connection failed")

        with self.assertRaises(MongoDBConnectionError) as context:
            MongoDBClient(uri="mock_uri", database_name=self.test_db_name)

        self.assertIn("Connection failed", str(context.exception))

    def test_get_collection_success(self):
        """
        Tests that an existing collection is returned successfully.
        """
        collection = self.client.get_collection(self.test_collection_name)
        self.mock_db.__getitem__.assert_called_with(self.test_collection_name)
        self.assertEqual(collection, self.mock_collection)

    def test_insert_document_success(self):
        """
        Tests that a document is inserted successfully.
        """
        test_document = {"key": "value"}
        inserted_id = "inserted_id"
        self.mock_collection.insert_one.return_value = MagicMock(
            inserted_id=inserted_id
        )

        result = self.client.insert_document(
            self.test_collection_name,
            test_document
        )

        self.mock_collection.insert_one.assert_called_once_with(test_document)
        self.assertEqual(result, inserted_id)

    def test_insert_document_failure(self):
        """
        Tests that MongoDBOperationError is raised when document insertion fails.
        """
        test_document = {"key": "value"}
        self.mock_collection.insert_one.side_effect = Exception("Insert failed")

        with self.assertRaises(MongoDBOperationError) as context:
            self.client.insert_document(self.test_collection_name, test_document)

        self.assertIn("Insert failed", str(context.exception))

    def test_find_documents_success(self):
        """
        Tests that documents are retrieved successfully.
        """
        test_query = {"key": "value"}
        mock_cursor = MagicMock()
        mock_documents = [{"_id": "1", "key": "value1"}, {"_id": "2", "key": "value2"}]
        mock_cursor.__iter__.return_value = iter(mock_documents)
        self.mock_collection.find.return_value = mock_cursor
        
        result = self.client.find_documents(self.test_collection_name, test_query)
        
        self.mock_collection.find.assert_called_once_with(test_query)
        self.assertEqual(result, mock_documents)

    def test_find_documents_failure(self):
        """
        Tests that MongoDBOperationError is raised when document retrieval fails.
        """
        test_query = {"key": "value"}
        self.mock_collection.find.side_effect = Exception("Find failed")

        with self.assertRaises(MongoDBOperationError) as context:
            self.client.find_documents(self.test_collection_name, test_query)

        self.assertIn("Find failed", str(context.exception))

    def test_update_document_success(self):
        """
        Tests that a document is updated successfully.
        """
        test_query = {"key": "value"}
        test_update_values = {"key": "new_value"}
        self.mock_collection.update_one.return_value = MagicMock(modified_count=1)

        result = self.client.update_document(
            self.test_collection_name, test_query, test_update_values
        )

        self.mock_collection.update_one.assert_called_once_with(
            test_query, {"$set": test_update_values}
        )
        self.assertEqual(result, 1)

    def test_update_document_failure(self):
        """
        Tests that MongoDBOperationError is raised when document update fails.
        """
        test_query = {"key": "value"}
        test_update_values = {"key": "new_value"}
        self.mock_collection.update_one.side_effect = Exception("Update failed")

        with self.assertRaises(MongoDBOperationError) as context:
            self.client.update_document(
                self.test_collection_name, test_query, test_update_values
            )

        self.assertIn("Update failed", str(context.exception))

    def test_delete_document_success(self):
        """
        Tests that a document is deleted successfully.
        """
        test_query = {"key": "value"}
        self.mock_collection.delete_one.return_value = MagicMock(deleted_count=1)

        result = self.client.delete_document(self.test_collection_name, test_query)

        self.mock_collection.delete_one.assert_called_once_with(test_query)
        self.assertEqual(result, 1)

    def test_delete_document_failure(self):
        """
        Tests that MongoDBOperationError is raised when document deletion fails.
        """
        test_query = {"key": "value"}
        self.mock_collection.delete_one.side_effect = Exception("Delete failed")

        with self.assertRaises(MongoDBOperationError) as context:
            self.client.delete_document(self.test_collection_name, test_query)

        self.assertIn("Delete failed", str(context.exception))

if __name__ == "__main__":
    unittest.main()