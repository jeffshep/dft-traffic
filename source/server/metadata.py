import json
import os

from get_data import read_column_headers, read_all_data

def metadata_parameter_response(param):
    if param =="ward_object_id":
        path = [os.path.dirname(__file__), 'static', f'ward_metadata.json']
        file_path = os.path.join(*path)
        ward_file = open(file_path)
        ward_json = json.load(ward_file)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "valid_values": ward_json
            })
        }

    else:
        data = read_all_data()
        unique_parameter_values = data[param].unique().tolist()
        return {
            "statusCode": 200,
            "body": json.dumps({
                "valid_values": sorted(unique_parameter_values)
            })
        }

def get_metadata_info(event):
    request_path = event.get('path', '')
    split_path = request_path.split('/')

    response = {
        "return_all_metadata": False
    }

    try:
        if len(split_path) == 3:
            response["param"] = split_path[2]
        elif split_path[1] == 'metadata':
            response["return_all_metadata"] = True
    except IndexError:
        pass
    
    return response

def metadata_response():

    road_data_column_headers = read_column_headers()
    
    base_parameters = ["ward_object_id"]

    metadata_parameters = base_parameters + road_data_column_headers

    return {
        "statusCode": 200,
        "body": json.dumps({
            "query_parameters": metadata_parameters,
            "additional_links": "https://storage.googleapis.com/dft-statistics/road-traffic/all-traffic-data-metadata.pdf"
        })
    }
    