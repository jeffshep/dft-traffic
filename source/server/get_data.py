import io
import json
import zipfile

import boto3

from pandas import read_csv

def read_raw_from_s3():
    s3_client = boto3.client("s3")
    response = s3_client.get_object(Bucket="packages-aadt", Key="dft_traffic_counts_aadf_by_direction.csv")
    
    return response.get("Body")

def read_all_data():
    response = read_raw_from_s3()
    return read_csv(response)

def read_column_headers():
    response = read_raw_from_s3()
    return read_csv(response, index_col=0, nrows=0).columns.tolist()    

def get_ward_data_from_s3(ward_id):
    s3 = boto3.resource('s3')

    bucket = s3.Bucket('packages-aadt')
    obj = bucket.Object('data_by_ward.zip')
    
    with io.BytesIO(obj.get()["Body"].read()) as tf:
        tf.seek(0)
        with zipfile.ZipFile(tf, mode='r') as zipf:
            for subfile in zipf.namelist():
                if subfile == f"data_by_ward/{ward_id}.geojson":
                    return json.loads(zipf.read(f"data_by_ward/{ward_id}.geojson"))