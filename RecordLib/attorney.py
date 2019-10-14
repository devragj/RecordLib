from dataclasses import dataclass



@dataclass
class Attorney:
    organization: str
    full_name: str
    organization_address: str
    organization_phone: str
    bar_id: str

    @staticmethod
    def from_dict(dct):
        return Attorney(**dct) 
    