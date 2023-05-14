from pymongo import MongoClient

connection_string = 'mongodb://localhost:27017/'
client = MongoClient(connection_string)

dbs = client.list_database_names()
test_db = client.test
collections = test_db.list_collection_names()


def insert_test_doc():
    collection = test_db.test
    test_document = {
        "name": "Tim",
        "Type": "Test",
    }
    inserted_id = collection.insert_one(test_document).inserted_id
    print(inserted_id)


production = client.production
person_collection = production.person_collection


def create_documents():
    first_names = ["Tim", "Sarah", "Jennifer", "Jose", "Brad", "Allen"]
    last_names = ["Ruscica", "Smith", "Bart", "Cater", "Pit", "Geral"]
    ages = [21, 40, 23, 19, 34, 67]

    docs = []

    for first_name, last_name, age in zip(first_names, last_names, ages):
        doc = {"first_name": first_name,
               "last_name": last_name,
               "age": age}
        docs.append(doc)

    person_collection.insert_many(docs)


def find_all_people():
    people = person_collection.find()
    for person in people:
        print(person)


def find_tim():
    tim = person_collection.find_one({"first_name": "Tim"})
    print(tim)


def count_all_people():
    count = person_collection.count_documents(filter={})
    print("Number of people: ", count)


def get_person_by_id(person_id):
    from bson.objectid import ObjectId

    _id = ObjectId(person_id)
    person = person_collection.find_one({"_id": _id})
    print(person)


def get_age_range(min_age, max_age):
    query = {"$and": [
        {"age": {"$gte": min_age}},
        {"age": {"$lte": max_age}}
    ]}
    people = person_collection.find(query).sort("age")
    for person in people:
        print(person)


def project_columns():
    columns = {"_id": 0, "first_name": 1, "last_name": 1}
    people = person_collection.find(filter={}, projection=columns)
    for person in people:
        print(person)


def update_person_by_id(person_id):
    from bson.objectid import ObjectId

    connection_string = 'mongodb://localhost:27017/'
    client = MongoClient(connection_string)
    production = client.production
    person_collection = production.person_collection

    _id = ObjectId(person_id)
    all_updates = {
        "$set": {"new_field": True},  # $set creates a new field or updates an existing field
        "$inc": {"age": 1},  # $inc increments a field by a specified amount
        "$rename": {"first_name": "first", "last_name": "last"}  # $rename renames a field
    }
    result = person_collection.update_one({"_id": _id}, all_updates).modified_count
    print(result)

    # person_collection.update_one({"_id": _id}, {"$unset": {"new_field": ""}})  # $unset deletes a field, it needs to be pass as a dictionary and the key is the field name, while the value is an empty string because doens't matter what the value is

# update_person_by_id("633c7b02e79b32ed126e0f5a")

def replace_one(person_id):
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)

    new_doc = {
        "first_name": "new_first_name",
        "last_name": "new_last_name",
        "age": 100
    }

    person_collection.replace_one({"_id": _id}, new_doc)


def delete_doc_by_id(person_id):
    from bson.objectid import ObjectId

    _id = ObjectId(person_id)
    person_collection.delete_one({"_id": _id})
    # person_collection.delete_many({})

# ----------------------------------------------------------------------------------------------------------------------

address = {
    "_id": "62f188b9cb4956de857dedb6",
    "street": "Bay Street",
    "number": 2706,
    "city": "San Francisco",
    "country": "United States",
    "zip": "94107",
}


def add_address_embed(person_id, address):
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)

    person_collection.update_one(
        {"_id": _id}, {"$addToSet": {"addresses": address}})  # $addToSet adds an element to an array if it doesn't already exist


def add_address_relationship(person_id, address):
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)

    address = address.copy()
    address["owner_id"] = person_id

    address_collection = production.address
    address_collection.insert_one(address)


# add_address_relationship("62f188b9cb4956de857dedb8", address)