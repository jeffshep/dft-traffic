from get_data import read_column_headers
from metadata import metadata_parameter_response, get_metadata_info, metadata_response
from queries import query_data

def handler(event, context):
    print(event)
    metadata = get_metadata_info(event)
    if metadata["return_all_metadata"]:
        return metadata_response()
    elif "param" in metadata:
        return metadata_parameter_response(metadata["param"])
    else:
        return query_data(event)

