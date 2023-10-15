import datetime

from pydantic import BaseModel
from typing import List


class CoordsDto(BaseModel):
    latitude1: float
    longitude1: float
    latitude2: float
    longitude2: float
    date: datetime.datetime


class AddressDto(BaseModel):
    address: str


class PersonStatusDto(BaseModel):
    person_status: str


class Coords(BaseModel):
    latitude: float
    longitude: float


class ServiceNecessity(BaseModel):
    coords: Coords
    entity: str
    feature: str
    full_mobility: bool
    services: List[str]
