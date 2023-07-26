import numpy as np
import pandas as pd
import pytest

from samsara.data import create_sequences, create_sliding_matrix

dates = ["2011-01-31", "2011-02-28", "2011-03-31", "2011-04-30", "2011-05-31"]
columns = ["TS-1", "TS-2", "TS-3", "TS-4", "TS-5"]
data = pd.DataFrame(
    np.array(
        [
            [1, 6, 8, 5, 0],
            [4, 4, 9, 3, 9],
            [2, 4, 0, 3, 5],
            [1, 1, 3, 4, 6],
            [3, 0, 6, 3, 8],
        ]
    ),
    index=dates,
    columns=columns,
)

exp_5_3 = np.array([[0, 1, 2], [1, 2, 3], [2, 3, 4]])
exp_6_4 = np.array([[0, 1, 2, 3], [1, 2, 3, 4], [2, 3, 4, 5]])
exp_10_5 = np.array(
    [
        [0, 1, 2, 3, 4],
        [1, 2, 3, 4, 5],
        [2, 3, 4, 5, 6],
        [3, 4, 5, 6, 7],
        [4, 5, 6, 7, 8],
        [5, 6, 7, 8, 9],
    ]
)


@pytest.mark.parametrize(
    "n_rows, seq_len, expected",
    [
        (5, 3, exp_5_3),
        (6, 4, exp_6_4),
        (10, 5, exp_10_5),
    ],
)
def test_create_sliding_matrix(n_rows, seq_len, expected):
    sliding_matrix = create_sliding_matrix(n_rows=n_rows, seq_len=seq_len)
    assert np.array_equal(sliding_matrix, expected)


def test_create_sequences():
    sequences, slide_dates, ts_indices = create_sequences(data, seq_len=3)
    expected_seqs = np.array(
        [
            [1, 4, 2],
            [6, 4, 4],
            [8, 9, 0],
            [5, 3, 3],
            [0, 9, 5],
            [4, 2, 1],
            [4, 4, 1],
            [9, 0, 3],
            [3, 3, 4],
            [9, 5, 6],
            [2, 1, 3],
            [4, 1, 0],
            [0, 3, 6],
            [3, 4, 3],
            [5, 6, 8],
        ]
    )
    expected_dates = np.array(
        [
            ["2011-01-31", "2011-02-28", "2011-03-31"],
            ["2011-01-31", "2011-02-28", "2011-03-31"],
            ["2011-01-31", "2011-02-28", "2011-03-31"],
            ["2011-01-31", "2011-02-28", "2011-03-31"],
            ["2011-01-31", "2011-02-28", "2011-03-31"],
            ["2011-02-28", "2011-03-31", "2011-04-30"],
            ["2011-02-28", "2011-03-31", "2011-04-30"],
            ["2011-02-28", "2011-03-31", "2011-04-30"],
            ["2011-02-28", "2011-03-31", "2011-04-30"],
            ["2011-02-28", "2011-03-31", "2011-04-30"],
            ["2011-03-31", "2011-04-30", "2011-05-31"],
            ["2011-03-31", "2011-04-30", "2011-05-31"],
            ["2011-03-31", "2011-04-30", "2011-05-31"],
            ["2011-03-31", "2011-04-30", "2011-05-31"],
            ["2011-03-31", "2011-04-30", "2011-05-31"],
        ],
    )

    expected_ts_indices = np.array(
        [
            "TS-1",
            "TS-2",
            "TS-3",
            "TS-4",
            "TS-5",
            "TS-1",
            "TS-2",
            "TS-3",
            "TS-4",
            "TS-5",
            "TS-1",
            "TS-2",
            "TS-3",
            "TS-4",
            "TS-5",
        ]
    )
    assert np.array_equal(sequences, expected_seqs)
    assert np.array_equal(slide_dates, expected_dates)
    assert np.array_equal(ts_indices, expected_ts_indices)
