import json
import os

from hamcrest import assert_that, has_key, equal_to, has_item
from mock import patch
from moto import mock_s3
from unittest import TestCase

from metadata import metadata_parameter_response, get_metadata_info, metadata_response

def file_path_to_data():
    path = [os.path.dirname(__file__), '..\\..\\data_prep', f'dft_traffic_counts_aadf_by_direction.csv']
    file_path = os.path.join(*path)
    return file_path

class TestMetadata(TestCase):
    def test_metadata_info_for_single_param_is_returned(self):
        event = {
            "path": "/metadata/year"
        }

        response = get_metadata_info(event)
        assert_that(response, equal_to({'return_all_metadata': False, 'param': 'year'}))

    def test_metadata_info_all_param_keys_returned(self):    
        event = {
            "path": "/metadata"
        }    

        response = get_metadata_info(event)

        assert_that(response, equal_to({'return_all_metadata': True}))

    def test_metadata_info_nothing_return_invalid_path(self):    
        event = {
            "path": "/something"
        }    

        response = get_metadata_info(event)

        assert_that(response, equal_to({'return_all_metadata': False}))

    @patch('get_data.read_raw_from_s3')
    @mock_s3
    def test_raw_data_metadata_is_returned(self, mock_raw_s3):
        mock_raw_s3.return_value = file_path_to_data()

        response = metadata_response()
        response_details = json.loads(response["body"])

        assert_that(response, has_key("statusCode"))
        assert_that(response, has_key("body"))
        assert_that(response_details["query_parameters"], has_item("ward_object_id"))
        assert_that(response_details["query_parameters"], has_item("hgvs_2_rigid_axle"))

    @patch('get_data.read_raw_from_s3')
    @mock_s3
    def test_metadata_parameter_year_response(self, mock_raw_s3):
        mock_raw_s3.return_value = file_path_to_data()

        response = metadata_parameter_response('year')
        response_details = json.loads(response["body"])

        assert_that(response_details["valid_values"], equal_to([2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]))

    def test_metadata_parameter_ward_response(self):

        response = metadata_parameter_response('ward_object_id')
        response_details = json.loads(response["body"])

        assert_that(len(response_details["valid_values"]["wards"]), equal_to(8694))

