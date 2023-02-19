import uuid
from pydantic import BaseModel, Field
from fastapi import HTTPException
from sqlalchemy import select
import datetime

from app.database import SessionLocal
from app.models import Apikey


class ApikeyBase(BaseModel):
    guid: uuid.UUID = Field(default_factory=uuid.uuid4)
    key: str

    async def validate(self) -> None | HTTPException:
        with SessionLocal() as session:
            stmt = (select(Apikey).where(Apikey.key == self.key).where(
                Apikey.expiry_at > datetime.datetime.utcnow().timestamp()))
            result = session.execute(stmt).scalar_one_or_none()
            if not result:
                raise HTTPException(status_code=401, detail='Unauthorised')
            
class ApikeyCreate(ApikeyBase):
    issued_at: int = Field(default_factory=datetime.datetime.now().timestamp)
    _duration: int = 1
    expiry_at: int = 0
    
    def __init__(self, **data):
        super().__init__(**data)
        self.expiry_at = self.issued_at + self._duration * 86400
    
class ApikeyRead(ApikeyCreate):
    def __init__(self):
        super().__init__(self)
        self.key = self.key[1:6] + '...'

class Apikey(ApikeyBase):
    id: int
    
    async def validate(self) -> None | HTTPException:
        super().validate(self)