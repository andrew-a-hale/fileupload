import uuid
from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.manifest import ManifestCreate, ManifestRead
import app.models as models

router = APIRouter()


@router.get('/manifest/{guid}', status_code=200, response_model=ManifestRead)
def get_manifest(guid: uuid.UUID, db: Session = Depends(get_db)):
    manifest = db.query(models.Manifest).where(models.Manifest.guid == guid).one_or_none()
    if not manifest:
        raise HTTPException(status_code=404, detail='Manifest not found')
    return manifest.__dict__


@router.post('/manifest', status_code=201, response_model=ManifestRead)
def add_manifest(response: Response, manifest: ManifestCreate, db: Session = Depends(get_db)):
    db_manifest = models.Manifest(**manifest.dict())
    db.add(db_manifest)
    db.commit()
    db.refresh(db_manifest)
    response['Content-Location'] = f'/manifest/{db_manifest.guid}'
    return db_manifest.__dict__


@router.delete('/manifest/{guid}', status_code=200)
def delete_manifest(guid: uuid.UUID, db: Session = Depends(get_db)):
    manifest = db.query(models.Manifest).where(models.Manifest.guid == guid).one_or_none()
    if not manifest:
        return Response(status_code=204, content=None)
    db.delete(manifest)
    db.commit()
    return {'message': f'manifest {guid} deleted'}