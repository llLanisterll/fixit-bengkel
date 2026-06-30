from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas
from database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Service])
def read_services(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_services(db, skip=skip, limit=limit)

@router.get("/{id}", response_model=schemas.Service)
def read_service(id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_service(db, id)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return db_obj

@router.post("/", response_model=schemas.Service)
def create_service(obj: schemas.ServiceCreate, db: Session = Depends(get_db)):
    return crud.create_service(db=db, service=obj)

@router.put("/{id}", response_model=schemas.Service)
def update_service(id: int, obj: schemas.ServiceCreate, db: Session = Depends(get_db)):
    return crud.update_service(db=db, service_id=id, service=obj)

@router.delete("/{id}")
def delete_service(id: int, db: Session = Depends(get_db)):
    crud.delete_service(db=db, service_id=id)
    return {"success": True}
