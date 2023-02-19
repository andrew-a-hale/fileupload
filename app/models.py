import datetime
import uuid
import enum

from sqlalchemy import ForeignKey, String, BigInteger, Enum, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, BYTEA


class Base(DeclarativeBase):
    pass


class Apikey(Base):
    __tablename__ = 'apikeys'

    id: Mapped[int] = mapped_column(primary_key=True)
    guid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True)
    key: Mapped[str] = mapped_column(String(40))
    expiry_at: Mapped[int] = mapped_column(BigInteger)
    issued_at: Mapped[int] = mapped_column(BigInteger)


class ManifestType(enum.Enum):
    CSV = 'csv'
    XLS = 'xls'
    XLSX = 'xlsx'
    JSON = 'json'
    XML = 'xml'
    PARQUET = 'parquet'


class Manifest(Base):
    __tablename__ = 'manifests'

    id: Mapped[int] = mapped_column(primary_key=True)
    guid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True)
    bucket_guid: Mapped[uuid.UUID] = mapped_column(ForeignKey('buckets.guid'))
    type: Mapped[ManifestType] = mapped_column(Enum(ManifestType))
    originator: Mapped[str] = mapped_column(String(50))
    agent: Mapped[str] = mapped_column(String(50))
    md5: Mapped[str] = mapped_column(String(500))
    filename: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now())


class BucketType(enum.Enum):
    S3 = 's3'
    LOCAL = 'local'
    DATABASE = 'database'


class Project(enum.Enum):
    PROJECT_A = 'project-a'
    PROJECT_B = 'project-b'
    PERSONAL = 'personal'


class Bucket(Base):
    __tablename__ = 'buckets'

    id: Mapped[int] = mapped_column(primary_key=True)
    guid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True)
    type: Mapped[BucketType] = mapped_column(Enum(BucketType))
    name: Mapped[str] = mapped_column(String(100))
    project: Mapped[Project] = mapped_column(Enum(Project))
    path: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now())

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": BucketType.LOCAL,
    }


class S3Bucket(Bucket):
    __mapper_args__ = {'polymorphic_identity': BucketType.S3}


class DbBucket(Bucket):
    __mapper_args__ = {'polymorphic_identity': BucketType.DATABASE}


class Payload(Base):
    __tablename__ = 'payloads'

    id: Mapped[int] = mapped_column(primary_key=True)
    guid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True)
    manifest_guid: Mapped[int] = mapped_column(ForeignKey('manifests.guid'))
    bucket_guid: Mapped[int] = mapped_column(ForeignKey('buckets.guid'))
    filename: Mapped[str] = mapped_column(String(100))
    content_type: Mapped[str] = mapped_column(String(50))
    md5: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now())


class Files(Base):
    __tablename__ = 'files'

    id: Mapped[int] = mapped_column(primary_key=True)
    guid: Mapped[int] = mapped_column(UUID(as_uuid=True), unique=True)
    manifest_guid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    bucket_guid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    payload: Mapped[bytes] = mapped_column(BYTEA)
    uploaded_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now())
