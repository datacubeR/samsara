import pandas as pd
import matplotlib.pyplot as plt


def analize_polygons(df_dict, name):
    """Function to Analyze results of the Preprocessing. Returns plots and Summaries.

    Parameters
    ----------
    df_dict : Dict
        Dictionary with all the preprocessed time Series in DataFrame format.
    name : Str
        Name of the Subset.
    """
    data = df_dict[name]

    IDs = pd.Series(data.index).str.split("-", expand=True)[2]
    resume = IDs.value_counts()
    resume.plot(
        kind="hist",
        bins=30,
        title=f"Number of Pixels by Polygon: {name}",
    )
    plt.show()
    print(f"Summary {name}")
    print(f"Dimensions: {data.shape}")
    print(f"Number of Null Values: {data.isnull().sum().sum()}")
    print("NA Summary:")
    print(data.isnull().sum().loc[lambda x: x > 0])
    print(f"Number of Polygons: {IDs.nunique()}")
    print(f"Number of TimeSteps for {name}: {data.shape[1]}")
    print(resume.agg(["min", "max", "mean", "median"]))
