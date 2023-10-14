import os

import uvicorn as uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import get_deps_in_coords, get_deps_by_address
from forms import CoordsDto, AddressDto

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
    return {"Status": os.getenv("STATUS")}


@app.get("/api/departments_in_coords")
async def departments_in_coords(coords: CoordsDto):
    return get_deps_in_coords(coords.latitude1, coords.longitude1, coords.latitude2, coords.longitude2)


@app.get("/api/department_by_address")
async def departments_in_coords(address_dto: AddressDto):
    return get_deps_by_address(address_dto.address)


if __name__ == "__main__":
    print("http://127.0.0.1:5000/api/")
    print("http://127.0.0.1:5000/api/departments_in_coords")
    print("http://127.0.0.1:5000/api/department_by_address")
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
