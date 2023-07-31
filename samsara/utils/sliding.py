import numpy as np


def create_sliding_matrix(n_rows, seq_len):
    """Crea una Sliding Matrix para vectorizar la creación de Secuencias de Entrenamiento.
    Basado en https://towardsdatascience.com/fast-and-robust-sliding-window-vectorization-with-numpy-3ad950ed62f5

    Parameters
    ----------
    n_rows : Número de Filas (Time Steps) de la Secuencia Total a Vectorizar.

    seq_len : Largo de la Secuencia de las Secuencias de Entrenamiento.


    Returns
    -------
    output : Sliding Matrix de la forma (n_rows - seq_len, seq_len)

    """
    max_value = n_rows - seq_len
    ## Doble Broadcasting
    output = (
        np.expand_dims(np.arange(seq_len), 0)
        + np.expand_dims(np.arange(max_value + 1), 0).T
    )
    return output


def create_sequences(df, seq_len, forecast=False):
    """Crea Secuencias de Entrenamiento a partir de un DataFrame de Multiples Series de Tiempo.

    Parameters
    ----------
    df : DataFrame con el formato (n_rows, n_cols) donde n_rows es largo de las Series de Tiempo
    y n_cols es el número de Series de Tiempo.

    seq_len : Largo de la Secuencia de las Secuencias de Entrenamiento.

    forecast: default = False. Para secuencias ReconstructionBased (forecast_values no debieran ser utilizados).
    Cambiar a True en el caso de ForecastBased y se eliminarán las secuencias que tengan un forecast_value = np.nan.

    Returns
    -------
    sequences : Secuencias de Entrenamiento de la forma (n_sequences, seq_len),
    donde n_sequences es el número de Secuencias de Entrenamiento.
    slide_dates: Corresponde a una Matriz asociada a las Fechas de las Secuencias Generadas (n_sequences, seq_len).
    ts_indices: Corresponde a un Vector asociado a los Indices de las Series de Tiempo, de las Secuencias Generadas. (n_sequences, )
    forecast_values: Valor asociado al forecast de cada secuencia generada. (n_sequences, ). Para el
    caso ReconstructionBased se debe eliminar las secuencias con forecast_values = np.nan.
    """
    n_rows, n_cols = df.shape
    if n_rows > seq_len:
        #
        dates = np.array(df.index)
        sliding_matrix = create_sliding_matrix(n_rows, seq_len)
        ts_indices = np.repeat(np.array(df.columns), n_cols)
        slide_dates = np.repeat(dates[sliding_matrix], n_cols, axis=0)
        sequences = (
            df.to_numpy()[sliding_matrix].transpose(0, 2, 1).reshape(-1, seq_len)
        )
        labels = df.to_numpy()[sliding_matrix[1:, -1]]
        nan_row = np.repeat(np.nan, labels.shape[1])
        forecast_values = np.vstack([labels, nan_row]).reshape(-1)
        ts_indices = np.repeat(
            np.array(df.columns).reshape(1, -1), len(sequences) / n_cols, axis=0
        ).flatten()

        if forecast:
            not_null = ~np.isnan(forecast_values)
            sequences = sequences[not_null]
            slide_dates = slide_dates[not_null]
            ts_indices = ts_indices[not_null]
            forecast_values = forecast_values[not_null]
        return sequences, slide_dates, ts_indices, forecast_values
    else:
        raise Exception(
            "Operación No válida: seq_len debe ser menor o igual al Número de Filas de df."
        )
