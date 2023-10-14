import os

import uvicorn as uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from database import get_deps_in_coords, get_deps_by_address, get_deps_by_open_status
from forms import CoordsDto, AddressDto, PersonStatusDto

load_dotenv()

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/api/')
async def get_items():
    return status.HTTP_200_OK


@app.post("/api/departments_in_coords")
async def departments_in_coords(coords: CoordsDto):
    return get_deps_in_coords(coords.latitude1, coords.longitude1, coords.latitude2, coords.longitude2)


@app.post("/api/department_by_address")
async def department_by_address(address_dto: AddressDto):
    return get_deps_by_address(address_dto.address)


@app.post("/api/department_by_open_status")
async def department_by_open_status(person_status_dto: PersonStatusDto):
    if person_status_dto.person_status not in ["lawyer", "individual"]:
        return
    return get_deps_by_open_status(person_status_dto.person_status)


if __name__ == "__main__":
    print("http://127.0.0.1:5000/api/")
    print("http://127.0.0.1:5000/api/departments_in_coords")
    print("http://127.0.0.1:5000/api/department_by_address")
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
