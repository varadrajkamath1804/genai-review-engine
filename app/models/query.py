from enum import Enum


class SortField(str, Enum):
    id = "id"
    confidence = "confidence"
    sentiment = "sentiment"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"
