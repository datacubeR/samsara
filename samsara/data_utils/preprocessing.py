def preprocessing(data, name, resample="W", i_method="linear", filter_id=None):
    """Applies the First Stage of Preprocessing for the Framework.

    Parameters
    ----------
    data : DataFrame
        Raw Data Imported from Parquet.
    resample : str, optional
        Resample Type, by default "W".
    i_method : str, optional
        Interpolation Type, by default "linear".
    filter_id : None, optional
        Filter out initial instances that cannot be Interpolated or Resampled, by default None.

    Returns
    -------
    DataFrame
        DataFrame with TimeSeries as Rows and Timestamps as columns.
    """
    data = data.resample(resample).mean().interpolate(method=i_method).T
    if filter_id is not None:
        data = data.iloc[:, filter_id:]
    print(
        f"Preprocessed data for {name}. {data.shape[0]} TimeSeries and {data.shape[1]} TimeStamps."
    )
    return data
