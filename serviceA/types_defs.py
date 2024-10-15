from typing import TypedDict, Dict


class TimeDict(TypedDict):
    updated: str
    updatedISO: str
    updateduk: str


class CurrencyDict(TypedDict):
    code: str
    rate: str
    description: str
    rate_float: float


class BitcoinPriceIndexResponse(TypedDict):
    time: TimeDict
    disclaimer: str
    bpi: Dict[str, CurrencyDict]
