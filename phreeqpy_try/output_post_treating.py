import os


def database_writer(output_data):
    output_data.__dict__()
    import pandas as pd
    pd_dataframe = pd.DataFrame(output_data)
    if not os.path.isdir("data"):
        os.mkdir("data")
    pd_dataframe.to_csv("/data/data_output.csv")
    return None
