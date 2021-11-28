from dataclasses import dataclass 

@dataclass(frozen=True)
class IBasicPersonDTO:
    # Person Data Transfer Object
    id: int
    name: str
    address: str
    phone: str