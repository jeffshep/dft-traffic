import json
import os

from mock import patch
from moto import mock_s3
from unittest import TestCase
from hamcrest import assert_that, has_key, equal_to, has_item

from queries import query_data

def file_path_to_data():
    path = [os.path.dirname(__file__), '..\\..\\data_prep', f'dft_traffic_counts_aadf_by_direction.csv']
    file_path = os.path.join(*path)
    return file_path

class TestQueries(TestCase):

    @patch('get_data.read_raw_from_s3')
    @mock_s3
    def test_multiple_query_parameters(self, mock_raw_s3):
        mock_raw_s3.return_value = file_path_to_data()
        
        event = {
            "path": "/",
            "queryStringParameters": {
                "year": 2011,
                "road_name": "A483"
            }
        }

        event = {
            "path": "/",
            "queryStringParameters": {
                "year": 2018
            }
        }

        response = query_data(event)
        response_details = json.loads(response["body"])
        
        # assert_that(response, has_key("statusCode"))
        # assert_that(response, has_key("body"))
        # assert_that(response_details, has_key("id"))     
        # assert_that(response_details, has_key("year"))