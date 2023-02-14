from sqlalchemy.orm import Session

from app.models import Apikey
from app.database import SessionLocal


def seed_api_keys(session: Session = SessionLocal()) -> None:
    with session:
        result = session.query(Apikey).first()
        if (result is None):
            key = Apikey(key="138c09b7-c9bc-49c3-bf0e-32e3186d9a17",
                         expiry=9999999999,
                         created_at=1676252381)
            session.add(key)
            session.commit()
            print("apikey seeded!")
