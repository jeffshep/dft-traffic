## AADT

## How to use the API
There are 2 request types to be aware of, these are described in more detail below.

All responses are in JSON format.

### Metadata
```
/aadf/metadata
```
This endpoint will return:
* All supported parameters in the raw data
* A third party link to additional information about parameter descriptions

```
/aadf/metadata/{parameter}
```

This endpoint will return all valid values for the requested parameter. This is intended to inform further requests with query strings.

For example: ```/aadf/metadata/road_name``` would return a list of road names that data is available for, so future requests can be targetted at known roads.

### Data
```
/aadf?road_name="M5"
```

This endpoint returns all data matching valid query string parameters.


### Ward queries

Administrative boundaries data, commonly known as Wards, available as a [direct download](https://opendata.arcgis.com/api/v3/datasets/95f1bc1b5da04522b086376a4acee322_0/downloads/data?format=geojson&spatialRefId=4326), is also available as a supplementary query parameter.

The metadata endpoint: `/aadf/metadata/ward_object_id` will return a list of wards containing both `id` and `name`, so that you can determine which id relates to the human-readable ward name, for subsequent requests.

The parameter `OBJECTID` is used to uniquely identify wards, therefore this is the value you should pass as the query string value for the ward you would like to query.

**If querying by ward, no other query parameters can be specified**

```/aadf?ward_object_id=1``` - for data that corresponds to the given ward



