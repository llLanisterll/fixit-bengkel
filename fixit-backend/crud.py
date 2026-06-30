from datetime import datetime
from sqlalchemy.orm import Session
import models, schemas
import time
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Users / Auth ---
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        password=hashed_password,
        role="CUSTOMER"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            update_data["password"] = pwd_context.hash(update_data["password"])
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# --- Services ---
def get_services(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Service).offset(skip).limit(limit).all()

def get_service(db: Session, service_id: int):
    return db.query(models.Service).filter(models.Service.id == service_id).first()

def create_service(db: Session, service: schemas.ServiceCreate):
    db_service = models.Service(**service.model_dump())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def update_service(db: Session, service_id: int, service: schemas.ServiceCreate):
    db_service = get_service(db, service_id)
    if db_service:
        for key, value in service.model_dump().items():
            setattr(db_service, key, value)
        db.commit()
        db.refresh(db_service)
    return db_service

def delete_service(db: Session, service_id: int):
    db_service = get_service(db, service_id)
    if db_service:
        db.delete(db_service)
        db.commit()
    return db_service

# --- Mechanics ---
def get_mechanics(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Mechanic).offset(skip).limit(limit).all()

def get_mechanic(db: Session, mechanic_id: int):
    return db.query(models.Mechanic).filter(models.Mechanic.id == mechanic_id).first()

def create_mechanic(db: Session, mechanic: schemas.MechanicCreate):
    db_mechanic = models.Mechanic(**mechanic.model_dump())
    db.add(db_mechanic)
    db.commit()
    db.refresh(db_mechanic)
    return db_mechanic

def update_mechanic(db: Session, mechanic_id: int, mechanic: schemas.MechanicCreate):
    db_mechanic = get_mechanic(db, mechanic_id)
    if db_mechanic:
        for key, value in mechanic.model_dump().items():
            setattr(db_mechanic, key, value)
        db.commit()
        db.refresh(db_mechanic)
    return db_mechanic

def delete_mechanic(db: Session, mechanic_id: int):
    db_mechanic = get_mechanic(db, mechanic_id)
    if db_mechanic:
        db.delete(db_mechanic)
        db.commit()
    return db_mechanic

# --- Spareparts ---
def get_spareparts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sparepart).offset(skip).limit(limit).all()

def get_sparepart(db: Session, sparepart_id: int):
    return db.query(models.Sparepart).filter(models.Sparepart.id == sparepart_id).first()

def create_sparepart(db: Session, sparepart: schemas.SparepartCreate):
    db_sparepart = models.Sparepart(**sparepart.model_dump())
    db.add(db_sparepart)
    db.commit()
    db.refresh(db_sparepart)
    return db_sparepart

def update_sparepart(db: Session, sparepart_id: int, sparepart: schemas.SparepartCreate):
    db_sparepart = get_sparepart(db, sparepart_id)
    if db_sparepart:
        for key, value in sparepart.model_dump().items():
            setattr(db_sparepart, key, value)
        db.commit()
        db.refresh(db_sparepart)
    return db_sparepart

def delete_sparepart(db: Session, sparepart_id: int):
    db_sparepart = get_sparepart(db, sparepart_id)
    if db_sparepart:
        db.delete(db_sparepart)
        db.commit()
    return db_sparepart

# --- Vehicles ---
def get_vehicles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vehicle).offset(skip).limit(limit).all()

def get_vehicle(db: Session, vehicle_id: int):
    return db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()

def create_vehicle(db: Session, vehicle: schemas.VehicleCreate):
    existing = db.query(models.Vehicle).filter(models.Vehicle.licensePlate == vehicle.licensePlate).first()
    if existing:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Kendaraan dengan plat nomor ini sudah terdaftar.")
    db_vehicle = models.Vehicle(**vehicle.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def update_vehicle(db: Session, vehicle_id: int, vehicle: schemas.VehicleCreate):
    existing = db.query(models.Vehicle).filter(models.Vehicle.licensePlate == vehicle.licensePlate, models.Vehicle.id != vehicle_id).first()
    if existing:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Kendaraan dengan plat nomor ini sudah terdaftar.")
    db_vehicle = get_vehicle(db, vehicle_id)
    if db_vehicle:
        for key, value in vehicle.model_dump().items():
            setattr(db_vehicle, key, value)
        db.commit()
        db.refresh(db_vehicle)
    return db_vehicle

def delete_vehicle(db: Session, vehicle_id: int):
    db_vehicle = get_vehicle(db, vehicle_id)
    if db_vehicle:
        db.delete(db_vehicle)
        db.commit()
    return db_vehicle

# --- Bookings ---
def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).order_by(models.Booking.id.desc()).offset(skip).limit(limit).all()

def get_booking(db: Session, booking_id: int):
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()

def create_booking(db: Session, booking: schemas.BookingCreate):
    # Conflict validation
    if booking.mechanicId:
        conflict = db.query(models.Booking).filter(
            models.Booking.mechanicId == booking.mechanicId,
            models.Booking.bookingDate == booking.bookingDate,
            models.Booking.timeSlot == booking.timeSlot,
            models.Booking.status != "CANCELLED"
        ).first()
        if conflict:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Mekanik tersebut sudah dibooking pada jam dan tanggal ini.")
    else:
        total_mechanics = db.query(models.Mechanic).count()
        busy = db.query(models.Booking).filter(
            models.Booking.bookingDate == booking.bookingDate,
            models.Booking.timeSlot == booking.timeSlot,
            models.Booking.status != "CANCELLED"
        ).count()
        if busy >= total_mechanics:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Semua mekanik sedang sibuk pada jam dan tanggal ini.")

    from sqlalchemy import func
    max_id = db.query(func.max(models.Booking.id)).scalar() or 0
    booking_code = f"FIX-{datetime.now().year}-{str(max_id + 1).zfill(4)}"
    
    # Extract serviceIds
    booking_dict = booking.model_dump()
    service_ids = booking_dict.pop("serviceIds", [])
    
    db_booking = models.Booking(**booking_dict, bookingCode=booking_code)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    # Add booking services
    if service_ids:
        services = db.query(models.Service).filter(models.Service.id.in_(service_ids)).all()
        for s in services:
            bs = models.BookingService(bookingId=db_booking.id, serviceId=s.id, priceAtBooking=s.price, quantity=1)
            db.add(bs)
        db.commit()

    return db_booking

def update_booking(db: Session, booking_id: int, booking: schemas.BookingCreate):
    db_booking = get_booking(db, booking_id)
    if db_booking:
        for key, value in booking.model_dump().items():
            setattr(db_booking, key, value)
        db.commit()
        db.refresh(db_booking)
    return db_booking

def delete_booking(db: Session, booking_id: int):
    db_booking = get_booking(db, booking_id)
    if db_booking:
        db.delete(db_booking)
        db.commit()
    return db_booking

# --- Service Logs ---
def get_service_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ServiceLog).offset(skip).limit(limit).all()

def get_service_log(db: Session, log_id: int):
    return db.query(models.ServiceLog).filter(models.ServiceLog.id == log_id).first()

def create_service_log(db: Session, log: schemas.ServiceLogCreate):
    db_log = models.ServiceLog(**log.model_dump())
    
    if log.sparepartId and log.sparepartQty > 0:
        db_sparepart = get_sparepart(db, log.sparepartId)
        if db_sparepart and db_sparepart.stock >= log.sparepartQty:
            db_sparepart.stock -= log.sparepartQty

    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

# --- Invoices ---
def get_invoices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Invoice).order_by(models.Invoice.id.desc()).offset(skip).limit(limit).all()

def get_invoice(db: Session, invoice_id: int):
    return db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()

def create_invoice(db: Session, invoice: schemas.InvoiceCreate):
    booking = db.query(models.Booking).filter(models.Booking.id == invoice.bookingId).first()
    if not booking:
        return None

    # Calculate costs
    service_cost = sum([bs.priceAtBooking * bs.quantity for bs in booking.bookingServices])
    
    sparepart_cost = 0
    for sl in booking.serviceLogs:
        if sl.sparepart:
            sparepart_cost += sl.sparepart.price * sl.sparepartQty

    total_cost = service_cost + sparepart_cost
    tax = total_cost * 0.1
    grand_total = total_cost + tax

    from sqlalchemy import func
    max_id = db.query(func.max(models.Invoice.id)).scalar() or 0
    invoice_number = f"INV-{datetime.now().year}-{str(max_id + 1).zfill(4)}"

    db_invoice = models.Invoice(
        invoiceNumber=invoice_number,
        bookingId=invoice.bookingId,
        serviceCost=service_cost,
        sparepartCost=sparepart_cost,
        totalCost=total_cost,
        tax=tax,
        grandTotal=grand_total
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def mark_invoice_paid(db: Session, invoice_id: int, payment_method: str):
    db_invoice = get_invoice(db, invoice_id)
    if db_invoice:
        db_invoice.paymentStatus = "PAID"
        db_invoice.paymentMethod = payment_method
        from datetime import datetime
        db_invoice.paidAt = datetime.utcnow()
        db.commit()
        db.refresh(db_invoice)
    return db_invoice
