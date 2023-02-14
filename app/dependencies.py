from fastapi import HTTPException, Header
from sqlalchemy import exists
import datetime

from app.database import SessionLocal
from app.models import Apikey

def get_db() -> None | HTTPException:
    try:
        db = SessionLocal()
        yield db
    except:
        HTTPException(status_code=503, detail="Could not establish connection to database")
    finally:
        db.close()

async def check_api_key(x_api_key: str | None = Header(default=None)) -> None | HTTPException:
    with SessionLocal() as session:
        stmt = exists(Apikey).where(Apikey.key == x_api_key).where(Apikey.expiry > datetime.datetime.utcnow().timestamp()).select()
        result = session.execute(stmt).scalar_one_or_none()
        if (result is False):
            raise HTTPException(status_code=401, detail="Unauthorised")
            