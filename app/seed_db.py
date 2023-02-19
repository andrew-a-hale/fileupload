import logging
import uuid
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine
from app.logger import log_decorator
from app.models import Base, Apikey, Bucket, BucketType, Manifest
from app.schemas.apikey import ApikeyCreate
from app.schemas.bucket import BucketCreate
from app.schemas.manifest import ManifestCreate


@log_decorator
def seed_api_keys(session: Session = SessionLocal()) -> None:
    with session:
        result = session.query(Apikey).first()
        if result is None:
            key = ApikeyCreate(key='138c09b7-c9bc-49c3-bf0e-32e3186d9a17',
                               duration=1)
            db_key = Apikey(**key.dict())
            session.add(db_key)
            session.commit()


@log_decorator
def seed_buckets(session: Session = SessionLocal()) -> None:
    with session:
        result = session.query(Bucket).first()
        if result is None:
            local_bucket = BucketCreate(
                guid=uuid.UUID('7e80e647-b98b-457c-b807-96cf1dd589e3'),
                type=BucketType.LOCAL,
                name='local_bucket',
                project='personal',
                path='.')
            s3_bucket = BucketCreate(
                guid=uuid.UUID('4fce0f33-73d9-41a7-9a51-f1e9859af91b'),
                type=BucketType.S3,
                name='s3_bucket',
                project='personal',
                path='.')
            db_bucket = BucketCreate(
                guid=uuid.UUID('40307b6c-869d-4c5d-a1f4-a37431ee4c64'),
                type=BucketType.DATABASE,
                name='db_bucket',
                project='personal',
                path='.')
            buckets = [local_bucket, s3_bucket, db_bucket]
            session.add_all([Bucket(**x.dict()) for x in buckets])
            session.commit()


@log_decorator
def seed_manifests(session: Session = SessionLocal()) -> None:
    with session:
        result = session.query(Manifest).first()
        if result is None:
            manifest = ManifestCreate(
                guid='6cec137d-019b-4737-83ef-920ab3e15ab3',
                type='csv',
                originator='Andrew',
                agent='Jason',
                md5='93eeb21b251ecccaf936b45dd7c3ef82',
                filename='file.csv',
                bucket_guid=uuid.UUID('7e80e647-b98b-457c-b807-96cf1dd589e3'))
            db_manifest = Manifest(**manifest.dict())
            session.add(db_manifest)
            session.commit()


@log_decorator
def setup_db() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    logging.info('db nuked!')
    seed_api_keys()
    seed_buckets()
    seed_manifests()
    logging.info('data seeded!')