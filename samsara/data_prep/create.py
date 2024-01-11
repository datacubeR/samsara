import numpy as np
from .sliding import create_sequential_data


def create_sequences(data, seq_len, step="Train", forecast_h=None):
    sequences = np.empty((0, seq_len))
    dates = np.empty((0, seq_len), dtype="datetime64[s]")
    indices = np.empty((0))
    targets = np.empty((0))
    target_dates = np.empty((0), dtype="datetime64[s]")
    target_indices = np.empty((0))

    for name, subset in data.items():
        (
            output_sequences,
            output_dates,
            output_indices,
            output_targets,
            output_target_dates,
            output_target_indices,
        ) = create_sequential_data(subset, seq_len, forecast_h=forecast_h)

        print(f"{step} Sequences for {name}: {output_sequences.shape[0]}")
        print("-----------------------------------------------------")

        sequences = np.concatenate([sequences, output_sequences])
        dates = np.concatenate([dates, output_dates])
        indices = np.concatenate([indices, output_indices])
        targets = np.concatenate([targets, output_targets])
        target_dates = np.concatenate([target_dates, output_target_dates])
        target_indices = np.concatenate([target_indices, output_target_indices])

    output_dict = {}
    output_dict["sequences"] = sequences
    output_dict["dates"] = dates
    output_dict["indices"] = indices
    output_dict["targets"] = targets if forecast_h is not None else None
    output_dict["target_dates"] = target_dates if forecast_h is not None else None
    output_dict["target_indices"] = target_indices if forecast_h is not None else None

    print("==========================================================")
    print(f"{output_dict['sequences'].shape[0]} total {step} sequences generated.")
    print(f"{output_dict['dates'].shape[0]} total {step} dates generated.")
    print(f"{output_dict['indices'].shape[0]} total {step} indices generated.")
    print("==========================================================")
    print(f"{output_dict['targets'].shape[0]} total {step} targets generated.")
    print(
        f"{output_dict['target_dates'].shape[0]} total {step} target dates generated."
    )
    print(
        f"{output_dict['target_indices'].shape[0]} total {step} target indices generated."
    )
    print("==========================================================")
    return output_dict
