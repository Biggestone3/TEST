from urllib.parse import quote_plus

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Encode username and password


def initialize(
    username: str,
    password: str,
    mongo_uri_part2: str,
) -> AsyncIOMotorClient:
    load_dotenv()
    mongo_uri_part1 = "mongodb+srv://"
    mongo_uri = get_mongo_uri(
        username=username,
        password=password,
        mongo_uri_part1=mongo_uri_part1,
        mongo_uri_part2=mongo_uri_part2,
    )

    return AsyncIOMotorClient(mongo_uri)


def get_mongo_uri(
    username: str,
    password: str,
    mongo_uri_part1: str,
    mongo_uri_part2: str,
) -> str:
    encoded_username = quote_plus(username)
    encoded_password = quote_plus(password)
    return mongo_uri_part1 + encoded_username + ":" + encoded_password + mongo_uri_part2
