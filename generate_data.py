from pymongo import MongoClient
from faker import Faker
import random

def generate_switchname():
    number = random.randint(10, 99)
    return f"deeeh-swt{number}"


def generate_hostname():
    number = random.randint(10000, 99999)
    return f"srv{number}"


def generate_interface():
    switchunit = random.randint(1, 4)
    port = random.randint(1, 48)
    interf = f"Gi{switchunit}/0/{port}"
    return interf


client = MongoClient('mongodb://root:example@localhost:27017/')
db = client['testdb']
collection = db['mac_db']

fake = Faker()


for _ in range(5000):
    dataset = {
        "mac": fake.mac_address(),
        "name": generate_hostname(),
        "switch": generate_switchname(),
        "port": generate_interface()
    }
    collection.insert_one(dataset)
    print(dataset)

