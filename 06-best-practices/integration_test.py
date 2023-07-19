from datetime import datetime
import os
import pandas as pd
from batch import get_input_path



def dt(hour, minute, second=0):

    return datetime(2022, 1, 1, hour, minute, second)


def test_integration_localstack():

    # create a dataframe to test
    data = [
        (None, None, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2), dt(1, 10)),
        (1, 2, dt(2, 2), dt(2, 3)),
        (None, 1, dt(1, 2, 0), dt(1, 2, 50)),
        (2, 3, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)

    # write the dataframe to S3 on localstack as an input file (in s3://nyc-duration/in/2022-01.parquet)
    end_point = os.getenv('S3_ENDPOINT_URL')

    if end_point is not None:
        options = {
           'client_kwargs': {
            'endpoint_url': end_point
           }
        }
        input_file = get_input_path(year=2022, month=1)
        df.to_parquet(
            input_file,
            engine="pyarrow",
            compression=None,
            index=False,
            storage_options=options
        )
    else:
        print("S3_ENDPOINT_URL is not set")


test_integration_localstack()


    








