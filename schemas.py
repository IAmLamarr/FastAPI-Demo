from enum import Enum
from pydantic import BaseModel


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class DogBase(BaseModel):
    name: str
    kind: DogType


class CreateDog(DogBase):
    pass


class Dog(DogBase):
    pk: int

    class Config:
        from_attributes = True


class Timestamp(BaseModel):
    id: int
    timestamp: int

    class Config:
        from_attributes = True
