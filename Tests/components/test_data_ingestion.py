import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from sensor.components.data_ingestion import DataIngestion
from sensor.datamodels.config import DataIngestionConfigEntity

class TestDataIngestion(unittest.TestCase):
    def setUp(self):
        self.config = DataIngestionConfigEntity(
            training_pipeline_config=MagicMock()
        )
        self.data_ingestion = DataIngestion(data_ingestion_config=self.config)

    @patch('sensor.components.data_ingestion.MongoDBClient')
    def test_export_data_to_feature_store(self, mock_mongo_client):
        mock_mongo_client.return_value.get_collection.return_value.find.return_value = [

        ]
        result = self.data_ingestion.export_data_to_feature_store()
        self.assertIsInstance(result, pd.DataFrame)

    @patch('sensor.components.data_ingestion.perform_train_test_split')
    @patch('sensor.components.data_ingestion.pd.DataFrame.to_csv')
    def test_split_data_into_train_test(self, mock_to_csv, mock_train_test_split):
        mock_train_test_split.return_value = (pd.DataFrame(), pd.DataFrame())
        dataframe = pd.DataFrame()
        self.data_ingestion.split_data_into_train_test(dataframe)
        self.assertTrue(mock_to_csv.called)

    @patch('sensor.components.data_ingestion.pd.read_csv')
    def test_read_fallback_csv(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame()
        result = self.data_ingestion._read_fallback_csv()
        self.assertIsInstance(result, pd.DataFrame)

    @patch('sensor.components.data_ingestion.os.makedirs')
    def test_create_feature_store_dir(self, mock_makedirs):
        self.data_ingestion._create_feature_store_dir()
        self.assertTrue(mock_makedirs.called)

    @patch('sensor.components.data_ingestion.pd.DataFrame.to_csv')
    def test_save_data_to_feature_store(self, mock_to_csv):
        data = pd.DataFrame()
        self.data_ingestion._save_data_to_feature_store(data)
        self.assertTrue(mock_to_csv.called)

if __name__ == '__main__':
    unittest.main()