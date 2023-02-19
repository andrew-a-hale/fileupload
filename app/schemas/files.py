import datetime
import uuid
from pydantic import BaseModel, Field


class FilesBase(BaseModel):
    guid: uuid.UUID = Field(default_factory=uuid.uuid4)
    payload: bytes


class FilesCreate(FilesBase):
    manifest_guid: uuid.UUID
    bucket_guid: uuid.UUID
    uploaded_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now)

    class Config:
        orm_mode = True

class FilesRead(FilesCreate):
    pass

class Files(FilesCreate):
    id: int

    class Config:
        orm_mode = True