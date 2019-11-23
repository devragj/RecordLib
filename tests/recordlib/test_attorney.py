from RecordLib.attorney import Attorney
from RecordLib.common import Address


def test_create_attorney():
    atty = Attorney(
        organization="Community Legal",
        full_name="John Smith",
        organization_address=Address(line_one="1234 Main St.", city_state_zip="Big City, NY 10002"),
        organization_phone="555-555-5555",
        bar_id="123456",
    )

    assert atty.organization == "Community Legal"
    assert atty.bar_id == "123456"
    assert atty.organization_address.city_state_zip == "Big City, NY 10002"
