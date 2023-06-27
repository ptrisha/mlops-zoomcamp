#!/usr/bin/env python
# coding: utf-8

import sys

import pickle
import pandas as pd
import numpy as np


with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)


categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


def run():

    year=int(sys.argv[1])
    month=int(sys.argv[2])

    # Read in data from Yellow Taxi Trip Records specifying year and month
    df = read_data(f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet')


    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)


    # Compute the standard deviation of the predicted duration
    print("Standard deviation of predicted duration:", "%.2f" % np.std(y_pred))

    # Compute the mean of the predicted duration
    print("Mean predicted duration:", "%.2f" % np.mean(y_pred))

    # We want to prepare the dataframe with the output of the prediction.

    # Create an artificial ride_id column
    df['ride_id']= f'{year:04d}/{month:02d}_' + df.index.astype('str')

    # Write the ride id and the predictions to a dataframe with results
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred

    # Save the results dataframe as a parquet file in the output folder
    output_file = f'/output/yellow_tripdur_{year:04d}-{month:02d}.parquet'
    df_result.to_parquet( output_file,
                        engine='pyarrow',
                        compression=None,
                        index=False
                        )


if __name__ == '__main__':
    run()





