from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn as uvicorn

from database import get_deps_in_coords, get_deps_by_address, get_deps_by_open_status, \
    get_atms_by_address, get_atms_in_coords, get_ten_nearest_departments, get_fullness_of_deps, get_fullness_of_dep
from forms import CoordsDto, AddressDto, PersonStatusDto, ServiceNecessity, FullnessDepDto

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
    deps = get_deps_in_coords(coords.latitude1, coords.longitude1, coords.latitude2, coords.longitude2)
    if len(deps) < 50:
        for dep_number in range(len(deps)):
            for measure in get_fullness_of_deps(coords.date):
                if deps[dep_number]["department_id"] == measure[1]:
                    deps[dep_number]["fullness"] = sum(measure[2:len(measure)]) / (len(measure) - 2)
                    if 0 <= deps[dep_number]["fullness"] <= 5.3:
                        deps[dep_number]["fullness"] = 0
                    if 5.3 < deps[dep_number]["fullness"] <= 5.9:
                        deps[dep_number]["fullness"] = 1
                    else:
                        deps[dep_number]["fullness"] = 2
                    break
    else:
        for dep_number in range(len(deps)):
            deps[dep_number]["fullness"] = -1
    return {"deps": deps,
            "atms": get_atms_in_coords(coords.latitude1, coords.longitude1, coords.latitude2, coords.longitude2)}


@app.post("/api/department_by_address")
async def department_by_address(address_dto: AddressDto):
    return {"deps": get_deps_by_address(address_dto.address),
            "atms": get_atms_by_address(address_dto.address)}


@app.post("/api/fullness_of_department")
async def fullness_of_department(fullness_dto: FullnessDepDto):
    fullness = get_fullness_of_dep(department_id=fullness_dto.department_id, date=fullness_dto.date)[0]
    fullness_avg = sum(fullness[2:len(fullness)]) / (len(fullness) - 2)
    if 0 <= fullness_avg <= 5.3:
        return 0
    if 5.3 < fullness_avg <= 5.9:
        return 1
    return 0


@app.post("/api/department_by_open_status")
async def department_by_open_status(person_status_dto: PersonStatusDto):
    if person_status_dto.person_status not in ["lawyer", "individual"]:
        return
    return get_deps_by_open_status(person_status_dto.person_status)


@app.post("/api/nearest_departments_by_coords")
async def department_by_open_status(service_necessity: ServiceNecessity):
    return get_ten_nearest_departments(service_necessity)


if __name__ == "__main__":
    print("http://127.0.0.1:5000/api/")
    print("http://127.0.0.1:5000/api/departments_in_coords")
    print("http://127.0.0.1:5000/api/department_by_address")
    print("http://127.0.0.1:5000/api/department_by_open_status")
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
