import os
import uuid
import logging
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.logger import log_debug_decorator
from app.schemas.files import FilesCreate
from app.schemas.payload import PayloadCreate
from app.models import BucketType, Files, Project

def bucket_model_to_schema(bucket_model):
    match bucket_model.type:
        case BucketType.LOCAL:
            bucket_class = Bucket
        case BucketType.S3:
            bucket_class = S3Bucket
        case BucketType.DATABASE:
            bucket_class = DbBucket
        case _:
            logging.error("Misconfigured bucket")
            raise Exception("Misconfigured bucket")
            
    return bucket_class.from_orm(bucket_model)

class BucketDoesNotExistError(ValueError):
    def __init__(self, message):
        super().__init__(self, message)
        self.message = message

class FileAlreadyUploadedError(OSError):

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class BucketBase(BaseModel):
    guid: uuid.UUID = Field(default_factory=uuid.uuid4)
    type: BucketType = BucketType.LOCAL
    name: str
    project: Project
    path: str

    @property
    def dir(self):
        dir = os.path.join(os.getenv('LOCAL_BUCKET_PATH'), self.project.value,
                           self.path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        return dir

    def send():
        pass


class BucketCreate(BucketBase):
    type: BucketType

class BucketRead(BucketCreate):
    pass

class Bucket(BucketBase):
    id: int
    type: BucketType = BucketType.LOCAL

    class Config:
        orm_mode = True

    @property
    def dir(self):
        dir = os.path.join(os.getenv('LOCAL_BUCKET_PATH'), self.project.value,
                           self.path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        return dir

    @log_debug_decorator
    def send(self, payload_metadata, payload, _):
        filepath = os.path.join(self.dir, payload_metadata.filename)

        if os.path.exists(filepath):
            raise FileAlreadyUploadedError(
                f'File: {payload_metadata.filename} already exists in this bucket'
            )

        with open(filepath, 'w') as file:
            file.write(payload.decode('utf-8'))


class S3Bucket(Bucket):
    id: int
    type: BucketType = BucketType.S3

    class Config:
        orm_mode = True

    @log_debug_decorator
    def send(self, payload_metadata, payload, _):
        print(f'{self.name} {payload_metadata.filename} {payload}')


class DbBucket(Bucket):
    id: int
    type: BucketType = BucketType.DATABASE

    class Config:
        orm_mode = True

    @log_debug_decorator
    def send(self, payload_metadata: PayloadCreate, payload: bytes,
             db: Session):
        result = (db.query(Files)
                  .where(Files.bucket_guid == payload_metadata.bucket_guid)
                  .where(Files.manifest_guid == payload_metadata.manifest_guid)
                  .one_or_none())
        if result:
            raise FileAlreadyUploadedError(
                f'File ({payload_metadata.filename}) already exists in this bucket'
            )
        file = FilesCreate(bucket_guid=payload_metadata.bucket_guid,
                           manifest_guid=payload_metadata.manifest_guid,
                           payload=payload)
        db_file = Files(**file.dict())
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
