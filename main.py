from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from db import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def root():
    return "success"


@app.post("/post", response_model=schemas.Timestamp)
def get_post(db: Session = Depends(get_db)):
    return crud.make_timestamp(db)


@app.post("/dog", response_model=schemas.Dog)
def create_dog(dog: schemas.CreateDog, db: Session = Depends(get_db)):
    return crud.create_dog(db, dog)


@app.get("/dog", response_model=list[schemas.Dog])
def get_dogs(db: Session = Depends(get_db), kind: schemas.DogType | None = None):
    return crud.get_dogs(db, kind)


@app.get("/dog/{pk}", response_model=schemas.Dog)
def get_dog_by_pk(pk: int, db: Session = Depends(get_db)):
    db_dog = crud.get_dog(db, pk)
    if db_dog is None:
        raise HTTPException(status_code=404, detail="Dog not found")
    return db_dog


@app.patch("/dog/{pk}", response_model=schemas.Dog)
def update_dog(dog: schemas.CreateDog, pk: int, db: Session = Depends(get_db)):
    db_dog = crud.get_dog(db, pk)
    if db_dog is None:
        raise HTTPException(status_code=404, detail="Dog not found")
    crud.update_dog(db, dog, pk)
    return crud.get_dog(db, pk)
