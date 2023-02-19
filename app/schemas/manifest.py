import uuid
from pydantic import BaseModel, Field

from app.models import ManifestType


class ManifestBase(BaseModel):
    guid: uuid.UUID = Field(default_factory=uuid.uuid4)
    type: ManifestType
    originator: str
    agent: str
    md5: str
    filename: str
    bucket_guid: uuid.UUID


class ManifestCreate(ManifestBase):
    pass

class ManifestRead(ManifestBase):
    pass

class Manifest(ManifestBase):
    id: int

    class Config:
        orm_mode = True
