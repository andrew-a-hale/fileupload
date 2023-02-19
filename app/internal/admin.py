from fastapi import APIRouter

router = APIRouter(prefix='/admin',
                   tags=['admin'])

@router.get('/')
def admin_root():
    return {'message': 'Admin Page'}
