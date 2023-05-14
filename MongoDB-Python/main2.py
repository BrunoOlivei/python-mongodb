from datetime import datetime as dt
from pymongo import MongoClient

connection_string = 'mongodb://localhost:27017/'
client = MongoClient(connection_string)

dbs = client.list_database_names()
production = client.production


def create_book_collection():
    book_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["title", "authors", "publish_date", "type", "copies"],
            "properties": {
                "title": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "authors": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "objectId",
                        "description": "must be a string and is required"
                    }
                },
                "publish_date": {
                    "bsonType": "date",
                    "description": "must be a date and is required"
                },
                "type": {
                    "enum": ["Fiction", "Non-Fiction"],
                    "description": "can only be one of the enum values and is required"
                },
                "copies": {
                    "bsonType": "int",
                    "minimum": 0,
                    "description": "must be an integer greater than 0 and is required"
                },
            }
        }
    }

    try:
        production.create_collection("book") # create collection
    except Exception as e:  # if collection already exists
        print(e)  # print error message

    production.command("collMod", "book", validator=book_validator)  # set validator - on Atlas needs to be run as admin


def create_author_collection():
    author_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["first_name", "last_name", "date_of_birth"],
            "properties": {
                "first_name": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "last_name": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "date_of_birth": {
                    "bsonType": "date",
                    "description": "must be a date and is required"
                },
            }
        }
    }

    try:
        production.create_collection("author")  # create collection
    except Exception as e:  # if collection already exists
        print(e)  # print error message

    production.command("collMod", "author", validator=author_validator)  # set validator - on Atlas needs to be run as admin


def create_data():
    authors = [
        {
            "first_name": "Tim",
            "last_name": "Ruscica",
            "date_of_birth": dt(2000, 7, 20)
        },
        {
            "first_name": "George",
            "last_name": "Orwell",
            "date_of_birth": dt(1903, 6, 25)
        },
        {
            "first_name": "Herman",
            "last_name": "Melville",
            "date_of_birth": dt(1819, 8, 1)
        },
        {
            "first_name": "F. Scott",
            "last_name": "Fitzgerald",
            "date_of_birth": dt(1896, 9, 24)
        }
    ]
    author_collection = production.author
    authors = author_collection.insert_many(authors).inserted_ids

    books = [
        {
            "title": "MongoDB: Advanced Tutorial",
            "authors": [authors[0]],
            "publish_date": dt.today(),
            "type": "Non-Fiction",
            "copies": 5
        },
        {
            "title": "Python for Dummies",
            "authors": [authors[0]],
            "publish_date": dt(2022, 1, 17),
            "type": "Non-Fiction",
            "copies": 5
        },
        {
            "title": "Nineteen Eighty-Four",
            "authors": [authors[1]],
            "publish_date": dt(1949, 6, 8),
            "type": "Fiction",
            "copies": 5
        },
        {
            "title": "The Great Gatsby",
            "authors": [authors[3]],
            "publish_date": dt(2014, 5, 23),
            "type": "Fiction",
            "copies": 5
        },
        {
            "title": "Moby Dick",
            "authors": [authors[2]],
            "publish_date": dt(1851, 9, 24),
            "type": "Fiction",
            "copies": 5
        }
    ]

    book_collection = production.book
    book_collection.insert_many(books)


create_data()