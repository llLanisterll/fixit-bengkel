from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas
from database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Sparepart])
def read_spareparts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_spareparts(db, skip=skip, limit=limit)

@router.get("/{id}", response_model=schemas.Sparepart)
def read_sparepart(id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_sparepart(db, id)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Sparepart not found")
    return db_obj

@router.post("/", response_model=schemas.Sparepart)
def create_sparepart(obj: schemas.SparepartCreate, db: Session = Depends(get_db)):
    return crud.create_sparepart(db=db, sparepart=obj)

@router.put("/{id}", response_model=schemas.Sparepart)
def update_sparepart(id: int, obj: schemas.SparepartCreate, db: Session = Depends(get_db)):
    return crud.update_sparepart(db=db, sparepart_id=id, sparepart=obj)

@router.delete("/{id}")
def delete_sparepart(id: int, db: Session = Depends(get_db)):
    crud.delete_sparepart(db=db, sparepart_id=id)
    return {"success": True}
