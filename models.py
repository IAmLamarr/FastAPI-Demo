from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum, Integer

from db import Base
from schemas import DogType


class Dog(Base):
    __tablename__ = "dogs"

    pk: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    kind: Mapped[DogType] = mapped_column(Enum(DogType))


class Timestamp(Base):
    __tablename__ = "timestamps"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[int] = mapped_column(Integer())
