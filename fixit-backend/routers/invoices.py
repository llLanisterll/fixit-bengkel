from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas
from database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Invoice])
def read_invoices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_invoices(db, skip=skip, limit=limit)

@router.get("/{id}", response_model=schemas.Invoice)
def read_invoice(id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_invoice(db, id)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return db_obj

@router.post("/", response_model=schemas.Invoice)
def create_invoice(obj: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    invoice = crud.create_invoice(db=db, invoice=obj)
    if not invoice:
        raise HTTPException(status_code=404, detail="Booking not found")
    return invoice

@router.put("/{id}", response_model=schemas.Invoice)
def mark_invoice_paid(id: int, payment_method: str = "CASH", db: Session = Depends(get_db)):
    return crud.mark_invoice_paid(db=db, invoice_id=id, payment_method=payment_method)
