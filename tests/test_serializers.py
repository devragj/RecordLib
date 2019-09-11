from RecordLib.serializers import to_serializable


def test_case_serialize(example_case):
    serialized = to_serializable(example_case)
    assert "docket_number" in serialized.keys()
    assert "otn" in serialized.keys()


def test_serialize_none():
    serialized = to_serializable(None)
    assert serialized == ""