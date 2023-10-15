import clickhouse_connect
import datetime
import pytz

from pymongo import MongoClient
from math import sqrt

from forms import ServiceNecessity

clickhouse_client = clickhouse_connect.get_client(host='154.194.53.172', port="8123", username="flints", password="moreflints")

conn_string = "mongodb://flints:moretechababa@154.194.53.172:27017"
client = MongoClient(conn_string)

database_name = "moretech"
department_collection = client[database_name]["departments"]
atms_collection = client[database_name]["atms"]
services_collection = client[database_name]["services"]

best_departments_count = 10


def get_department(department_id):
    return department_collection.find_one({"department_id": department_id}, {'_id': False})


def get_atm(atm_id):
    return atms_collection.find_one({"atm_id": atm_id}, {'_id': False})


def get_all_services():
    return services_collection.find({{'_id': False}})


def get_deps_in_coords(latitude1: float, longitude1: float, latitude2: float, longitude2: float):
    return list(department_collection.find({"latitude": {"$lt": latitude1, "$gt": latitude2},
                                            "longitude": {"$gt": longitude1, "$lt": longitude2}},
                                           {'_id': False}))


def get_atms_in_coords(latitude1: float, longitude1: float, latitude2: float, longitude2: float):
    return list(atms_collection.find({"latitude": {"$lt": latitude1, "$gt": latitude2},
                                      "longitude": {"$gt": longitude1, "$lt": longitude2}},
                                     {'_id': False}))


def get_deps_by_address(address: str):
    return list(
        department_collection.find({"$or": [{"address": {"$regex": address}}, {"salePointName": {"$regex": address}}]},
                                   {'_id': False}))


def get_atms_by_address(address: str):
    return list(
        atms_collection.find({"$or": [{"address": {"$regex": address}}, {"salePointName": {"$regex": address}}]},
                             {'_id': False}))


def get_deps_by_open_status(person_status: str):
    current_datetime = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    all_deps = list(department_collection.find({}, {'_id': False}))

    opened_deps = []
    hours_for_person_status = ""
    if person_status == "lawyer":
        hours_for_person_status = "openHours"
    elif person_status == "individual":
        hours_for_person_status = "openHoursIndividual"

    for dep in all_deps:
        if len(dep[hours_for_person_status]) == 7 and \
                dep[hours_for_person_status][current_datetime.weekday()]["hours"] != "выходной":
            current_hours_schedule = dep[hours_for_person_status][current_datetime.weekday()]["hours"]

            start_time, end_time = current_hours_schedule.split('-')

            start_time_hours, start_time_minutes = start_time.split(':')
            start_time_hours = start_time_hours.strip('0')
            start_time = datetime.time(int(start_time_hours), int(start_time_minutes), 0)

            end_time_hours, end_time_minutes = end_time.split(':')
            end_time_hours = end_time_hours.strip('0')
            end_time = datetime.time(int(end_time_hours), int(end_time_minutes), 0)

            d = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
            start_time = datetime.datetime.combine(d, start_time)
            end_time = datetime.datetime.combine(d, end_time)

            if start_time.timestamp() <= current_datetime.timestamp() <= end_time.timestamp():
                opened_deps.append(dep)
    return opened_deps


def get_ten_nearest_departments(service_necessity: ServiceNecessity):
    dep_filter = list()
    dep_filter.append({"full_mobility": service_necessity.full_mobility})
    if service_necessity.entity != "":
        dep_filter.append({"entity": service_necessity.entity})
    if service_necessity.feature != "":
        dep_filter.append({"feature": service_necessity.feature})

    departments = department_collection.find({"$and": dep_filter})

    result = list()
    for department in departments:
        services = department["services"]
        if check_on_services(service_necessity.services, services):
            result.append({
                "id": department["department_id"],
                "distance": get_distance(service_necessity.coords.latitude, service_necessity.coords.longitude,
                                         department["latitude"], department["longitude"])
            })
    result = result[:best_departments_count]
    result_departments = list()
    for res in result:
        result_departments.append(department_collection.find_one({"department_id": res["id"]}, {'_id': False}))
    return result_departments


def check_on_services(services: list, all_services: list):
    res = True
    for service in services:
        res = res and check_on_service(service, all_services)
    return res


def check_on_service(check_service: str, all_services: list):
    for service in all_services:
        if service["name"] == check_service:
            return True
    return False


def get_distance(x_1: float, y_1: float, x_2: float, y_2: float):
    return sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)


def get_fullness_of_dep(date):
    result = clickhouse_client.query(f"SELECT * FROM clients WHERE toDayOfWeek(datetime) == {date.weekday() + 1} AND toHour(datetime) == {date.hour}")
    return result.result_rows


if __name__ == "__main__":
    pass
    # By coords
    # deps = get_deps_in_coords(
    #     latitude1=200.0,
    #     longitude1=10.124,
    #     latitude2=0.012380,
    #     longitude2=100.124,
    # )

    # By address
    # deps = get_deps_by_address("Зеленоградский» Филиала")

    # By open status
    # deps = get_deps_by_open_status("individual")
    # for i in deps:
    #     print(deps)

    # Get atm
    # print(get_atm(750))

    print(get_fullness_of_dep(datetime.datetime.now()))
