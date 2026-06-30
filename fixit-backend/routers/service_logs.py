from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas
from database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.ServiceLog])
def read_service_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_service_logs(db, skip=skip, limit=limit)

@router.get("/{id}", response_model=schemas.ServiceLog)
def read_service_log(id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_service_log(db, id)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="ServiceLog not found")
    return db_obj

@router.post("/", response_model=schemas.ServiceLog)
def create_service_log(obj: schemas.ServiceLogCreate, db: Session = Depends(get_db)):
    return crud.create_service_log(db=db, log=obj)
