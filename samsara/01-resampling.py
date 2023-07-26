import argparse
from pathlib import Path

from loguru import logger

from data import import_raw_data

RESAMPLE_PATH = Path("data/resample/")
RESAMPLE_PATH.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--resample", "-r", choices=["W", "2W", "M"], required=True)
    argparser.add_argument(
        "--interpolate", "-i", choices=["linear", "time", "ff", "bf"], required=True
    )
    args = argparser.parse_args()

    logger.info(
        f"Procesando Datos Resampling: {args.resample}, Interpolación: {args.interpolate}."
    )
    logger.info("Importando Datos Raw...")
    df_dict = import_raw_data()

    for event, data in df_dict.items():
        output = (
            data.resample(args.resample).mean().interpolate(method=args.interpolate)
        )
        seq_len, n_ts = output.shape
        logger.success(f"Resampling {event}: {n_ts} TSs de largo {seq_len}.")
        output.to_parquet(
            RESAMPLE_PATH
            / f"resample_{event}_{args.resample}_{args.interpolate}.parquet",
            index=False,
        )

    logger.success("Datos Resampleados e Interpolados con éxito.")

# print(f"Null Values: {df_interpolated.isnull().sum().sum()}")
#
# SEQ_LEN = 5
# dates = np.array(pd.date_range(start="2019-01-01", end="2020-01-01", freq="M"))
# df = pd.DataFrame(
#     np.random.randint(0, 10, size=(12, 2)),
#     index=dates,
#     columns=["ESTABLE-1", "ESTABLE-2"],
# )
# sequences, slide_dates, ts_indices = create_sequences(df, SEQ_LEN)
