from pymongo import MongoClient

conn_string = "mongodb://filipp:creator_of_the_world_1232122@77.240.39.113:27017"
client = MongoClient(conn_string)

database_name = "moretech"
department_collection = client[database_name]["department_collection"]


def get_statistics():
    return department_collection.find_one({}, {'_id': False})


def create_department(address, capacity):
    department_collection.insert_one({
        "department_id": department_collection.count_documents({}),
        "address": address,
        "capacity": capacity,
    })
