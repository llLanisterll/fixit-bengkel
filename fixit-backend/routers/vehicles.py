from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas
from database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Vehicle])
def read_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_vehicles(db, skip=skip, limit=limit)

@router.get("/{id}", response_model=schemas.Vehicle)
def read_vehicle(id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_vehicle(db, id)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_obj

@router.post("/", response_model=schemas.Vehicle)
def create_vehicle(obj: schemas.VehicleCreate, db: Session = Depends(get_db)):
    return crud.create_vehicle(db=db, vehicle=obj)

@router.put("/{id}", response_model=schemas.Vehicle)
def update_vehicle(id: int, obj: schemas.VehicleCreate, db: Session = Depends(get_db)):
    return crud.update_vehicle(db=db, vehicle_id=id, vehicle=obj)

@router.delete("/{id}")
def delete_vehicle(id: int, db: Session = Depends(get_db)):
    crud.delete_vehicle(db=db, vehicle_id=id)
    return {"success": True}
