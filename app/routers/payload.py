import hashlib
import uuid
from fastapi import APIRouter, Form, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi import Depends, UploadFile

from app.dependencies import get_db
from app.schemas.bucket import FileAlreadyUploadedError, BucketDoesNotExistError, bucket_model_to_schema
from app.schemas.payload import PayloadCreate, PayloadRead
from app import models

router = APIRouter()


@router.get('/payload/{guid}', status_code=200, response_model=PayloadRead)
def get_payload(guid: uuid.UUID, db: Session = Depends(get_db)):
    payload = db.query(models.Payload).where(models.Payload.guid == guid).one_or_none()
    if not payload:
        raise HTTPException(status_code=404, detail='Payload not found')
    return payload


@router.post('/payload', status_code=201, response_model=PayloadRead)
async def add_payload(file: UploadFile, manifest_guid: uuid.UUID = Form(), bucket_guid: uuid.UUID = Form(), db: Session = Depends(get_db)):
    
    # read file + form
    content = await file.read()
    db_manifest = db.query(models.Manifest).where(models.Manifest.guid == manifest_guid).one_or_none()
    db_bucket = db.query(models.Bucket).where(models.Bucket.guid == bucket_guid).one_or_none()
    
    if not db_manifest:
        raise HTTPException(status_code=400, detail="Manifest not found")
        
    if not db_bucket:
        raise HTTPException(status_code=400, detail="Bucket not found")
    
    # create and validate payload
    payload = PayloadCreate(manifest_guid=manifest_guid,
                              manifest_md5=db_manifest.md5,
                              manifest_filename=db_manifest.filename,
                              bucket_guid=bucket_guid,
                              filename=file.filename,
                              content_type=file.content_type,
                              md5=hashlib.md5(content).hexdigest())
    
    # upload to bucket            
    try:
        bucket = bucket_model_to_schema(db_bucket)
        bucket.send(payload, content, db)
    except FileAlreadyUploadedError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except BucketDoesNotExistError as e:
        raise HTTPException(status_code=500, detail=e.message)
    
    # insert payload record into db
    db_payload = models.Payload(guid=payload.guid, manifest_guid=manifest_guid, bucket_guid=bucket_guid, filename=payload.filename, content_type=payload.content_type, md5=payload.md5)
    db.add(db_payload)
    db.commit()
    db.refresh(db_payload)
    
    return db_payload.__dict__


@router.delete('/payload/{guid}', status_code=200)
def delete_payload(guid: uuid.UUID, db: Session = Depends(get_db)):
    payload = db.query(models.Payload).where(models.Payload.guid == guid).one_or_none()
    if not payload:
        return Response(status_code=204, content=None)
    db.delete(payload)
    db.commit()
    return {'message': f'payload {guid} deleted'}