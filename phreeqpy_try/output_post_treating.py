import os
import pandas as pd


def database_creator(output_data):
    output_data = dict(output_data)
    pd_dataframe = pd.DataFrame(output_data)
    return pd_dataframe


def database_writer(dataframe):
    if not os.path.isdir("data"):
        os.mkdir("data")
    dataframe.to_csv("/data/data_output.csv")
    return None
