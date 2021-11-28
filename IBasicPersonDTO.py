from dataclasses import dataclass 

@dataclass(frozen=True)
class IBasicPersonDTO:
    id: int
    name: str
    address: str
    phone: str