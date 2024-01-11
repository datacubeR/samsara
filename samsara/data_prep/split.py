def split_idx(df_dict, date="2018-01-01"):
    idx = df_dict["ESTABLE"].columns >= date
    train_indices = df_dict["ESTABLE"].columns[~idx]
    test_indices = df_dict["ESTABLE"].columns[idx]
    return train_indices, test_indices


def split_data(df_dict, paths, date="2018-01-01"):
    train_indices, test_indices = split_idx(df_dict, date=date)
    train_df_dict = {}
    test_df_dict = {}
    for name in paths.keys():
        train_df_dict[name] = df_dict[name][train_indices]
        test_df_dict[name] = df_dict[name][test_indices]
    return train_df_dict, test_df_dict
