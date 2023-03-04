import uuid
from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.bucket import BucketCreate, BucketRead
from app import models

router = APIRouter()


@router.get('/bucket/{guid}', status_code=200, response_model=BucketRead)
def get_bucket(guid: uuid.UUID, db: Session = Depends(get_db)):
    bucket = db.query(
        models.Bucket).where(models.Bucket.guid == guid).one_or_none()
    if not bucket:
        raise HTTPException(status_code=404, detail='Bucket not found')
    return bucket.__dict__


@router.post('/bucket', status_code=201, response_model=BucketRead)
def add_bucket(bucket: BucketCreate, db: Session = Depends(get_db)):
    # check if bucket already exists
    result = db.query(
        models.Bucket).where(models.Bucket.guid == bucket.guid).one_or_none()
    if result:
        raise HTTPException(status_code=400,
                            detail='Bucket with this id already exists')

    # add bucket
    db_bucket = models.Bucket(**bucket.dict())
    db.add(db_bucket)
    db.commit()
    db.refresh(db_bucket)
    return db_bucket.__dict__


@router.delete('/bucket/{guid}', status_code=200)
def delete_bucket(guid: uuid.UUID, db: Session = Depends(get_db)):
    bucket = db.query(
        models.Bucket).where(models.Bucket.guid == guid).one_or_none()
    if not bucket:
        return Response(status_code=204, content=None)
    db.delete(bucket)
    db.commit()
    return {'message': f'bucket {guid} deleted'}