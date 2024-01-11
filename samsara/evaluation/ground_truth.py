import pandas as pd


def create_ground_truth(aux_paths, cols_to_keep):
    data_list = []
    for name, path in aux_paths.items():
        data = pd.read_csv(path)[cols_to_keep]
        data["NAME"] = name
        data_list.append(data)
    ground_truth = pd.concat(data_list).reset_index(drop=True)
    return ground_truth


def fix_dates(df, col="Finicio", date="19/082006", fix="19/08/2006"):
    idx = df.query(f"{col} =='{date}'").index
    df[col] = df[col].str.replace(date, fix)
    return df


def convert_dates(df):
    df["Finicio"] = pd.to_datetime(df["Finicio"], dayfirst=True)
    df["Fultima"] = pd.to_datetime(df["Fultima"], dayfirst=True)
    return df
