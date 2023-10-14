import json
from pymongo import MongoClient

conn_string = "mongodb://flints:moretechababa@154.194.53.172:27017"
client = MongoClient(conn_string)

database_name = "moretech"
atms_collection = client[database_name]["atms"]


def create_atm(address, latitude, longitude, allDay, wheelchair, blind, nfcForBankCards, qrRead,
                      supportsUsd, supportsChargeRub, supportsEur, supportsRub):
    atms_collection.insert_one({
        "atm_id": atms_collection.count_documents({}),
        "address": address,
        "latitude": latitude,
        "longitude": longitude,
        "allDay": allDay,
        "wheelchair": wheelchair,
        "blind": blind,
        "nfcForBankCards": nfcForBankCards,
        "qrRead": qrRead,
        "supportsUsd": supportsUsd,
        "supportsChargeRub": supportsChargeRub,
        "supportsEur": supportsEur,
        "supportsRub": supportsRub,
    })


with open("../atms.txt", "r", encoding='utf-8') as f:
    all_atms = json.loads(f.read())
    for atm in all_atms["atms"]:
        create_atm(
            address=atm["address"],
            latitude=atm["latitude"],
            longitude=atm["longitude"],
            allDay=atm["allDay"],
            wheelchair=atm["services"]["wheelchair"],
            blind=atm["services"]["blind"],
            nfcForBankCards=atm["services"]["nfcForBankCards"],
            qrRead=atm["services"]["qrRead"],
            supportsUsd=atm["services"]["supportsUsd"],
            supportsChargeRub=atm["services"]["supportsChargeRub"],
            supportsEur=atm["services"]["supportsEur"],
            supportsRub=atm["services"]["supportsRub"]
        )
