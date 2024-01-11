import pandas as pd


def import_data(name, aux_paths, paths):
    """Import data from Parquet format.

    Parameters
    ----------
    name : Str
        Name of the Subset.
    AUX_PATHS : Dict, optional
        Dictionary with Auxiliary Paths, by default AUX_PATHS
    PATHS : Dict, optional
        Dictionary with Data Paths, by default PATHS

    Returns
    -------
    DataFrame
        DataFrame with TimeStamps as Rows and TimeSeries IDs as Columns.
    """
    data_aux = pd.read_csv(aux_paths[name])[["IDpix", "ID"]]
    data = (
        pd.read_parquet(paths[name])
        .merge(data_aux, on="IDpix", how="left")
        .assign(
            full_ID=lambda x: name + "-" + x.IDpix.astype(str) + "-" + x.ID.astype(str)
        )
        .drop(columns=["IDpix", "ID"])
        .set_index("full_ID")
        .T
    )
    data.index = data.index.astype("datetime64[ns]")
    print(
        f"Importing {data.shape[0]} timestamps and {data.shape[1]} Time Series for {name}."
    )
    return data
