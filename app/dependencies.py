from fastapi import HTTPException, Header

from app.database import SessionLocal
from app.schemas.apikey import ApikeyBase

def get_db() -> None | HTTPException:
    try:
        db = SessionLocal()
        yield db
    except:
        HTTPException(status_code=503, detail='Could not establish connection to database')
    finally:
        db.close()

async def check_api_key(x_api_key: str | None = Header(default=None)) -> None | HTTPException:
    if not x_api_key:
        raise HTTPException(status_code=401, detail='Unauthorised')
    api_key = ApikeyBase(key=x_api_key)
    api_key.validate()
            