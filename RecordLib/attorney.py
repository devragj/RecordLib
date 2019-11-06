from dataclasses import dataclass
from RecordLib.common import Address


@dataclass
class Attorney:
    organization: str
    full_name: str
    organization_address: Address
    organization_phone: str
    bar_id: str

    @staticmethod
    def from_dict(dct):
        dct["address"] = Address.from_dict(dct.get("address"))
        return Attorney(**dct) 
