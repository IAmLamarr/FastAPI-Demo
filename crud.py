from datetime import datetime
import time

from sqlalchemy import update
from sqlalchemy.orm import Session

import models
import schemas


def make_timestamp(db: Session):
    timestamp = time.mktime(datetime.now().timetuple())
    db_timestamp = models.Timestamp(timestamp=timestamp)
    db.add(db_timestamp)
    db.commit()
    db.refresh(db_timestamp)
    return db_timestamp


def get_dog(db: Session, dog_id: int):
    return db.query(models.Dog).filter(models.Dog.pk == dog_id).first()


def get_dogs(db: Session, kind: schemas.DogType | None = None):
    dogs = db.query(models.Dog)
    if kind:
        dogs = dogs.filter(models.Dog.kind == kind)
    return dogs.all()


def create_dog(db: Session, dog: schemas.CreateDog):
    db_dog = models.Dog(**dog.model_dump())
    db.add(db_dog)
    db.commit()
    db.refresh(db_dog)
    make_timestamp(db)
    return db_dog


def update_dog(db: Session, dog: schemas.CreateDog, pk):
    stmt = (update(models.Dog)
            .where(models.Dog.pk == pk)
            .values(**dog.model_dump()))
    db.execute(stmt)
    make_timestamp(db)
    return get_dog(db, pk)
