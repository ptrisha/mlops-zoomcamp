from datetime import datetime
import pandas as pd
from batch import prepare_data


def dt(hour, minute, second=0):

    return datetime(2022, 1, 1, hour, minute, second)


def test_prepare_data():

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
    df_transformed = prepare_data(df, columns)
    print("transformed df:")
    print(df_transformed)

    exp_transformed = [
        (None, None, dt(1, 2), dt(1, 10), 8.0),
        (1, None, dt(1, 2), dt(1, 10), 8.0),
        (1, 2, dt(2, 2), dt(2, 3), 1.0),
    ]
    exp_columns = columns + ['duration']
    exp_df = pd.DataFrame(exp_transformed, columns=exp_columns)
    exp_df[columns] = exp_df[columns].fillna(-1).astype('int').astype('str')
    print('expected df:')
    print(exp_df)

    assert df_transformed.equals(exp_df)


