from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- User & Auth ---
class UserBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class User(UserBase):
    id: int
    role: str
    createdAt: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str# --- Service ---
class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = "ROUTINE"
    price: float
    estimatedMinutes: Optional[int] = 60
    isActive: Optional[bool] = True

class ServiceCreate(ServiceBase):
    pass

class Service(ServiceBase):
    id: int

    class Config:
        from_attributes = True

# --- Mechanic ---
class MechanicBase(BaseModel):
    name: str
    phone: Optional[str] = None
    specialization: Optional[str] = None
    photo: Optional[str] = None
    status: Optional[str] = "AVAILABLE"

class MechanicCreate(MechanicBase):
    pass

class Mechanic(MechanicBase):
    id: int
    createdAt: datetime

    class Config:
        from_attributes = True

# --- Sparepart ---
class SparepartBase(BaseModel):
    name: str
    partNumber: str
    brand: Optional[str] = None
    stock: Optional[int] = 0
    price: float
    unit: Optional[str] = "pcs"
    minStock: Optional[int] = 5

class SparepartCreate(SparepartBase):
    pass

class Sparepart(SparepartBase):
    id: int

    class Config:
        from_attributes = True

# --- Vehicle ---
class VehicleBase(BaseModel):
    userId: int
    brand: str
    model: str
    year: int
    licensePlate: str
    color: Optional[str] = None

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int
    createdAt: datetime

    class Config:
        from_attributes = True

# --- Booking ---
class BookingBase(BaseModel):
    userId: int
    vehicleId: int
    mechanicId: Optional[int] = None
    bookingDate: datetime
    timeSlot: str
    status: Optional[str] = "PENDING"
    notes: Optional[str] = None

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    bookingCode: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True

# --- ServiceLog ---
class ServiceLogBase(BaseModel):
    bookingId: int
    mechanicId: int
    sparepartId: Optional[int] = None
    description: str
    sparepartQty: Optional[int] = 0
    status: Optional[str] = "STARTED"

class ServiceLogCreate(ServiceLogBase):
    pass

class ServiceLog(ServiceLogBase):
    id: int
    logDate: datetime

    class Config:
        from_attributes = True

# --- Invoice ---
class InvoiceBase(BaseModel):
    bookingId: int
    paymentStatus: Optional[str] = "UNPAID"
    paymentMethod: Optional[str] = None

class InvoiceCreate(BaseModel):
    bookingId: int

class Invoice(InvoiceBase):
    id: int
    invoiceNumber: str
    serviceCost: float
    sparepartCost: float
    totalCost: float
    tax: float
    grandTotal: float
    paidAt: Optional[datetime] = None
    createdAt: datetime

    class Config:
        from_attributes = True
