import os
import json
def main():
    path = [os.path.dirname(__file__), 'static', 'Wards_May_2021_UK_BFE.geojson']
    file_path = os.path.join(*path)
    ward_file = open(file_path)
    ward_data = json.load(ward_file)

    ward_info = []
    for feature in ward_data["features"]:
        ward_info.append(
            {
                "id": feature["properties"]["OBJECTID"],
                "name": feature["properties"]["WD21NM"]
            }
        )
    
    output_data = {
        "wards": ward_info
    }

    path = [os.path.dirname(__file__), 'static', f'ward_metadata.json']
    file_path = os.path.join(*path)

    with open(file_path, 'w') as f:
        json.dump(output_data, f)
main()        