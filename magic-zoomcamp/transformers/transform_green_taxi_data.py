import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    print("Rows with zero passenger:", data['passenger_count'].isin([0]).sum())
        
    column_mapping = {
        'VendorID': 'vendor_id',
        'RatecodeID': 'ratecode_id',
        'PULocationID': 'pulocation_id',
        'DOLocationID': 'dolocation_id'
    }

    data.rename(columns=column_mapping, inplace=True)

    existing_vendor_ids = set(data['vendor_id'].unique())
    
    # Convert 'lpep_pickup_datetime' to datetime
    data['lpep_pickup_datetime'] = pd.to_datetime(data['lpep_pickup_datetime'])

    # Create 'lpep_pickup_date' column by extracting date from 'lpep_pickup_datetime'
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    #all data must be above 0
    data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]
    
    # Filter rows with non-positive passenger counts and trip distances
    transformed_data = data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]
    
    # Assertions
    assert set(transformed_data['vendor_id']).issubset(existing_vendor_ids), "vendor_id contains values not in the existing values"
    assert (transformed_data['passenger_count'] > 0).all(), "passenger_count contains non-positive values"
    assert (transformed_data['trip_distance'] > 0).all(), "trip_distance contains non-positive values"

    # Print or return the final data after assertions
    print("Data is successfully asserted into variable: transformed_data")
    
    data = transformed_data
    
    return data