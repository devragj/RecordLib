from RecordLib.attorney import Attorney


def test_create_attorney():
    atty = Attorney(
        organization = "Community Legal",
        name = "John Smith",
        organization_address = r"1234 Main St.\nBig City, NY 10002",
        organization_phone = "555-555-5555",
        bar_id = "123456",
    )

    assert atty.organization == "Community Legal"
    assert atty.bar_id == "123456"