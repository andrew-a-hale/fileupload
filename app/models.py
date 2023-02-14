from sqlalchemy import String, Integer, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Apikey(Base):
    __tablename__ = "apikeys"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(40))
    expiry: Mapped[int] = mapped_column(BigInteger)
    created_at: Mapped[int] = mapped_column(BigInteger)


class Manifest(Base):
    __tablename__ = "manifests"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(10))
    originator: Mapped[str] = mapped_column(String(50))
    agent: Mapped[str] = mapped_column(String(50))
    md5: Mapped[str] = mapped_column(String(500))
    filename: Mapped[str] = mapped_column(String(100))
    filesize: Mapped[int] = mapped_column(Integer)