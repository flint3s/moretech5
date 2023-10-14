from pydantic import BaseModel


class CoordsDto(BaseModel):
    latitude1: float
    longitude1: float
    latitude2: float
    longitude2: float


class AddressDto(BaseModel):
    address: str
