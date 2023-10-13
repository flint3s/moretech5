import json
from pymongo import MongoClient

conn_string = "mongodb://filipp:creator_of_the_world_1232122@77.240.39.113:27017"
client = MongoClient(conn_string)

database_name = "moretech"
department_collection = client[database_name]["department_collection"]


def get_statistics():
    return department_collection.find_one({}, {'_id': False})


def create_department(address, salePointName, openHours, rko, openHoursIndividual, officeType, salePointFormat,
                      suoAvailability, hasRamp, latitude, longitude, metroStation, distance, kep, myBranch):
    department_collection.insert_one({
        "department_id": department_collection.count_documents({}),
        "address": address,
        "salePointName": salePointName,
        "openHours": openHours,
        "rko": rko,
        "openHoursIndividual": openHoursIndividual,
        "officeType": officeType,
        "salePointFormat": salePointFormat,
        "suoAvailability": suoAvailability,
        "hasRamp": hasRamp,
        "latitude": latitude,
        "longitude": longitude,
        "metroStation": metroStation,
        "distance": distance,
        "kep": kep,
        "myBranch": myBranch
    })


with open("offices.txt", "r", encoding='utf-8') as f:
    all_deps = json.loads(f.read())
    for dep in all_deps:
        create_department(
            address=dep["address"],
            salePointName=dep["salePointName"],
            openHours=dep["openHours"],
            rko=dep["rko"],
            openHoursIndividual=dep["openHoursIndividual"],
            officeType=dep["officeType"],
            salePointFormat=dep["salePointFormat"],
            suoAvailability=dep["suoAvailability"],
            hasRamp=dep["hasRamp"],
            latitude=dep["latitude"],
            longitude=dep["longitude"],
            metroStation=dep["metroStation"],
            distance=dep["distance"],
            kep=dep["kep"],
            myBranch=dep["myBranch"],
        )
