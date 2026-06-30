from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas
from database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Booking])
def read_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_bookings(db, skip=skip, limit=limit)

@router.get("/{id}", response_model=schemas.Booking)
def read_booking(id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_booking(db, id)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_obj

@router.post("/", response_model=schemas.Booking)
def create_booking(obj: schemas.BookingCreate, db: Session = Depends(get_db)):
    return crud.create_booking(db=db, booking=obj)

@router.put("/{id}", response_model=schemas.Booking)
def update_booking(id: int, obj: schemas.BookingCreate, db: Session = Depends(get_db)):
    return crud.update_booking(db=db, booking_id=id, booking=obj)

@router.delete("/{id}")
def delete_booking(id: int, db: Session = Depends(get_db)):
    crud.delete_booking(db=db, booking_id=id)
    return {"success": True}
