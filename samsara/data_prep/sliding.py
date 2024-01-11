import numpy as np


def create_sliding_matrix(n_timestamps, seq_len):
    """Crea una Sliding Matrix para vectorizar la creación de Secuencias de Entrenamiento.
    Basado en https://towardsdatascience.com/fast-and-robust-sliding-window-vectorization-with-numpy-3ad950ed62f5

    Parameters
    ----------
    n_timestamps : Number of timestamps of the Sequences to vectorize.
    seq_len : Sequence Length to vectorize.


    Returns
    -------
    output : Sliding Matrix of shape (n_timestamp - seq_len, seq_len)

    """
    max_value = n_timestamps - seq_len
    ## Double Broadcasting
    output = (
        np.expand_dims(np.arange(seq_len), 0)
        + np.expand_dims(np.arange(max_value + 1), 0).T
    )
    return output


def create_sequential_data(df, seq_len, forecast_h=None):
    """Generates the sequential data needed for Modeling.

    Parameters
    ----------
    df : DataFrame
        DataFrame of shape (n_timeseries, n_timestamps), where n_timeseries corresponds to the number of Timeseries in the dataset, whereas n_timestamps corresponds to the number of timestamps.
    seq_len : int
        Length of the Sequences we want to generate.
    forecast_h : int, optional
        Forecast Horizon to generate targets if needed, by default None. If Forecast Horizon is None then targets and target_dates are None.

    Returns
    -------
    tuple
        sequences: Sequences generated of shape (n_seq, seq_len). n_seq corresponds to the resulting number of sequences generated.
        slide_dates: Corresponding Dates for the generated sequences. Shape (n_seq, seq_len).
        ts_indices: Corresponding TimeSeries Indices for the generated Indices. Shape (n_seq, )
        targets: Target in case that a Forecast Horizon is provided. None if forecast_h is None. Shape (n_seq-n_timeseries, )
        target_dates: Corresponding dates for the Target. Shape (n_seq-n_timeseries, )
        target_indices: Corresponding TimeSeries indices for the Target. Shape (n_seq-n_timeseries, )

    """
    # Working with the Transpose for compatibility.
    df = df.T
    n_timestamps, n_timeseries = df.shape
    if n_timestamps > seq_len:
        #
        dates = np.array(df.index)
        sliding_matrix = create_sliding_matrix(n_timestamps, seq_len)
        ts_indices = np.repeat(np.array(df.columns), n_timeseries)
        slide_dates = np.repeat(dates[sliding_matrix], n_timeseries, axis=0)
        sequences = (
            df.to_numpy()[sliding_matrix].transpose(0, 2, 1).reshape(-1, seq_len)
        )
        ts_indices = np.repeat(
            np.array(df.columns).reshape(1, -1), len(sequences) / n_timeseries, axis=0
        ).flatten()
        targets = None
        target_dates = None
        target_indices = None

        if forecast_h is not None:
            extended_sliding_matrix = create_sliding_matrix(
                n_timestamps, seq_len + forecast_h
            )
            targets = (
                df.to_numpy()[extended_sliding_matrix]
                .transpose(0, 2, 1)
                .reshape(-1, seq_len + forecast_h)[:, -1]
            )
            target_dates = np.repeat(
                dates[extended_sliding_matrix], n_timeseries, axis=0
            )[:, -1]
            n_targets = targets.shape[0]
            target_indices = ts_indices[:n_targets]
            sequences = sequences[:n_targets]
            slide_dates = slide_dates[:n_targets]
            ts_indices = ts_indices[:n_targets]

        return sequences, slide_dates, ts_indices, targets, target_dates, target_indices

    else:
        print(
            "Operación No válida: seq_len debe ser menor o igual al Número de Filas de df."
        )
        return None, None, None, None, None
