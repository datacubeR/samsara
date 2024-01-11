def validate_dimensions(data, forecast=False):
    assert (
        data["sequences"].shape[0] == data["dates"].shape[0] == data["indices"].shape[0]
    )

    if forecast:
        assert (
            data["sequences"].shape[0]
            == data["targets"].shape[0]
            == data["target_dates"].shape[0]
            == data["target_indices"].shape[0]
        )
