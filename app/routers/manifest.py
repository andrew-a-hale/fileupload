from fastapi import APIRouter, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi import Depends

from app.dependencies import get_db
from app import schemas
from app import models

router = APIRouter()


@router.get("/manifest/{manifest_id}", status_code=200)
def get_manifest(manifest_id: int, db: Session = Depends(get_db)):
    manifest = db.get(models.Manifest, manifest_id)
    if (manifest is None):
        raise HTTPException(status_code=404, detail="Data not found")
    return manifest


@router.post("/manifest", status_code=201)
def add_manifest(manifest: schemas.ManifestCreate,
                 db: Session = Depends(get_db)):
    db_manifest = models.Manifest(**manifest.dict())
    db.add(db_manifest)
    db.commit()
    db.refresh(db_manifest)
    return db_manifest


@router.delete("/manifest/{manifest_id}", status_code=200)
def delete_manifest(manifest_id: int, db: Session = Depends(get_db)):
    manifest = db.get(models.Manifest, manifest_id)
    if (manifest is None):
        return Response(status_code=204, content=None)
    db.delete(manifest)
    db.commit()
    return {"message": f"manifest {manifest_id} deleted"}