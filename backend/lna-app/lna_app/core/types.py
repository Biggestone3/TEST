"""Core types and enums used across the application."""

from enum import Enum
from typing import Annotated
from uuid import UUID

from pydantic import PlainSerializer


class Language(str, Enum):
    """Language options for content."""

    ENGLISH = "en"
    ARABIC = "ar"
    UNKNOWN = "unknown"


# Custom type that maintains UUID type safety internally but serializes to string
# in API responses. This ensures consistent UUID handling across the application
# while providing clean string-based UUIDs in JSON responses and MongoDB storage.
UUIDstr = Annotated[UUID, PlainSerializer(lambda x: str(x), return_type=str)]
