import json
from pymongo import MongoClient

conn_string = "mongodb://flints:moretechababa@154.194.53.172:27017"
client = MongoClient(conn_string)

database_name = "moretech"
department_collection = client[database_name]["departments"]


def get_statistics():
    return department_collection.find_one({}, {'_id': False})


def get_deps_in_coords(latitude1, longitude1, latitude2, longitude2):
    return list(department_collection.find({"latitude": {"$lt": latitude1, "$gt": latitude2},
                                            "longitude": {"$gt": longitude1, "$lt": longitude2}},
                                           {'_id': False}))


if __name__ == "__main__":
    deps = get_deps_in_coords(
        latitude1=200.0,
        longitude1=10.124,
        latitude2=0.012380,
        longitude2=100.124,
    )
