from fastapi import APIRouter, Depends

from app.dependencies import check_api_key

router = APIRouter(prefix="/admin",
                   tags=["admin"],
                   dependencies=[Depends(check_api_key)])


@router.get("/")
def admin_root():
    return {"message": "Admin Page"}