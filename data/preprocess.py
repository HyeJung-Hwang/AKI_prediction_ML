import pandas as pd
import numpy as np


def preprocess(nonvital_path : str = "",vital_path : str = "",vital_key : str = ""):
    nonvital_df_Y = pd.read_csv(nonvital_path + "df_meta_Y.csv")
    nonvital_df_Y["caseid"] = nonvital_df_Y["file_id"].apply(lambda x: x.split(".")[0])
    nonvital_df_N = pd.read_csv(nonvital_path + "df_meta_N.csv")
    nonvital_df_N["caseid"] = nonvital_df_N["file_id"].apply(lambda x: x.split(".")[0])
    vital_df_Y = pd.read_csv( vital_path + vital_key+"_Y.csv" )
    vital_df_N = pd.read_csv( vital_path + vital_key+"_N.csv" )

    # merge non vital data & vital data
    df_N_44 = pd.merge(vital_df_N, nonvital_df_N, on='caseid', how='left')
    df_Y_44 = pd.merge(vital_df_Y, nonvital_df_Y, on='caseid', how='left')

    df = pd.concat([df_N_44, df_Y_44])
    df = df.drop(
        ["Unnamed: 0_x", "Unnamed: 0_y", "caseid", "patient_num", "Serial_number", "file_id", "department", "op_date"],
        axis=1)

    # masking
    df["sex"] = df["sex"].map({"male": 0, "female": 1})
    df["AKI"] = df["AKI"].map({"N": 0, "Y": 1})
    df["high_AKI"] = df["high_AKI"].map({"N": 0, "Y": 1})
    df["op_name"] = df["op_name"].map(
        {v: k for k, v in dict(enumerate(df["op_name"].value_counts().reset_index()["index"])).items()}
    )

    df = df.astype(float)
    df = df.sample(frac=1).reset_index(drop=True)
    return df