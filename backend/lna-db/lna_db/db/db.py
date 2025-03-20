from urllib.parse import quote_plus
from pymongo import MongoClient
from datetime import UTC, datetime
from uuid import UUID

from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient, AsyncMongoMockDatabase
from motor.motor_asyncio import AsyncIOMotorClient

from lna_db.core.types import Language
from lna_db.models.news import AggregatedStory, Article, Source
# Encode username and password
def initialize():
    username = "bna14"
    password = "Ottovan@20"

    encoded_username = quote_plus(username)
    encoded_password = quote_plus(password)

    # Replace the placeholders with the encoded values
    mongo_uri = f"mongodb+srv://{encoded_username}:{encoded_password}@bahaaammourydatabase1.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"


    client = MongoClient(mongo_uri)

    # Create a new database
    # db = client["my_db"]

    # article = db["articles"]
    # user = db["users"]
    # source = db["sources"]
    # aggregatedStory = db['aggregatedStories']
    return AsyncIOMotorClient(mongo_uri)
    

# import pandas as pd
# import time
# def write_to_db(df, collection, unique_field):
#     df = df.dropna(how='all')  # Remove empty rows

#     if df.empty:
#         print(f"Warning: df is empty. Skipping insert.")
#         return

#     data = df.to_dict(orient="records")  # Convert to list of dictionaries

#     # Extract unique values to delete in bulk
#     unique_values = [doc[unique_field] for doc in data]

#     if unique_values:
#         collection.delete_many({unique_field: {"$in": unique_values}})  # Delete in bulk

#     if data:
#         collection.insert_many(data)  # Bulk insert

#     print(f"Processed {len(data)} records into {collection.name}.")
# def read_from_db(collection, key="NULL", value="NULL"):
#     if key == "NULL" and value=="NULL":
#         result = collection.find()
    
#     elif key!="NULL" and value!="NULL":
#         result = collection.find({key: value})

#     else:
#         raise ValueError("Invalid key or value: one or both are NULL")
    
#     return result


# # Example to add data to a collection
# """
# You will be having a (df) as an output of a crawler

# Function Call:
#     write_to_db(df,article,'UUID')
# """


# # Example to view data in a collection
# """
# Read all available articles

# Function Call:
#     read_from_db(article)
# """


# # Search for certain source article
# """
# Function Call:
#     read_from_db(article,'source','exampleSource')
# """

