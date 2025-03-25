from urllib.parse import quote_plus
from pymongo import MongoClient
from datetime import UTC

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

# Encode username and password
def initialize():
    username = "bna14"
    password = "Ottovan@20"

    encoded_username = quote_plus(username)
    encoded_password = quote_plus(password)

    # Replace the placeholders with the encoded values
    mongo_uri = f"mongodb+srv://{encoded_username}:{encoded_password}@bahaaammourydatabase1.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"


    client = MongoClient(mongo_uri)
    return AsyncIOMotorClient(mongo_uri)