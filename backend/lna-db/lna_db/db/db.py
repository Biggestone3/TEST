import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


# Encode username and password
def initialize() -> AsyncIOMotorClient:
    load_dotenv()
    username = str(os.environ.get("username_of_db"))
    password = str(os.environ.get("password_of_db"))
    encoded_username = quote_plus(username)
    encoded_password = quote_plus(password)
    mongo_uri_part1 = str(os.environ.get("mongo_uri_part1"))
    mongo_uri_part2 = str(os.environ.get("mongo_uri_part2"))
    mongo_uri = (
        mongo_uri_part1 + encoded_username + ":" + encoded_password + mongo_uri_part2
    )

    return AsyncIOMotorClient(mongo_uri)
