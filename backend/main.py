import os

import uvicorn as uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import get_deps_in_coords
from forms import CoordsDto

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


if __name__ == "__main__":
    print("http://127.0.0.1:5000/api/")
    print("http://127.0.0.1:5000/api/departments_in_coords")
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
