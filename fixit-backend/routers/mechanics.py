from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas
from database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Mechanic])
def read_mechanics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_mechanics(db, skip=skip, limit=limit)

@router.get("/{{id}}", response_model=schemas.Mechanic)
def read_mechanic(id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_mechanic(db, id)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Mechanic not found")
    return db_obj

@router.post("/", response_model=schemas.Mechanic)
def create_mechanic(obj: schemas.MechanicCreate, db: Session = Depends(get_db)):
    return crud.create_mechanic(db=db, mechanic=obj)

@router.put("/{{id}}", response_model=schemas.Mechanic)
def update_mechanic(id: int, obj: schemas.MechanicCreate, db: Session = Depends(get_db)):
    return crud.update_mechanic(db=db, mechanic_id=id, mechanic=obj)

@router.delete("/{{id}}")
def delete_mechanic(id: int, db: Session = Depends(get_db)):
    crud.delete_mechanic(db=db, mechanic_id=id)
    return {{"success": True}}
