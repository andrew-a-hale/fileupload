from typing import Literal
from pydantic import BaseModel
from enum import Enum

class Apikey(BaseModel):
    id: int
    key: str
    expiry: int
    created_at: int

class ManifestType(Enum):
    CSV = "csv"
    XLS = "xls"
    XLSX = "xlsx"
    JSON = "json"
    XML = "xml"
    PARQUET = "parquet"

class ManifestBase(BaseModel):
    type: Literal['csv', 'xls', 'xlsx', 'json', 'xml', 'parquet']
    originator: str
    agent: str
    md5: str
    filename: str
    filesize: int

class ManifestCreate(ManifestBase):
    pass

class Manifest(ManifestBase):
    id: int