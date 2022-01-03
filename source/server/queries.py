import json

from get_data import read_all_data, get_ward_data_from_s3

def query_data(event):
    query_params = event.get('queryStringParameters', {})

    if "ward_object_id" in query_params.keys():
        ward_id = str(query_params["ward_object_id"])
        data = get_ward_data_from_s3(ward_id)        
        return {
            "statusCode": 200,
            "body": json.dumps(data)
        }
    else:
        data = read_all_data()
        print(query_params.keys())
        print (data.head())

        for param in query_params.keys():
            
            data = data.loc[data[param] == query_params[param]]
            print(data)
            

        return {
            "statusCode": 200,
            "body": data.to_json()
        }