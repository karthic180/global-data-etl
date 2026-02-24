def test_sample_transform():
    data = {"value": 10}
    # Example: multiply value by 2
    transformed = {"value": data["value"] * 2}
    assert transformed["value"] == 20