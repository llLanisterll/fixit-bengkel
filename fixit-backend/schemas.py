from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- Base Models ---
class UserBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None

class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = "ROUTINE"
    price: float
    estimatedMinutes: Optional[int] = 60
    isActive: Optional[bool] = True

class MechanicBase(BaseModel):
    name: str
    phone: Optional[str] = None
    specialization: Optional[str] = None
    photo: Optional[str] = None
    status: Optional[str] = "AVAILABLE"

class SparepartBase(BaseModel):
    name: str
    partNumber: str
    brand: Optional[str] = None
    stock: Optional[int] = 0
    price: float
    unit: Optional[str] = "pcs"
    minStock: Optional[int] = 5

class VehicleBase(BaseModel):
    userId: int
    brand: str
    model: str
    year: int
    licensePlate: str
    color: Optional[str] = None

class BookingBase(BaseModel):
    userId: int
    vehicleId: int
    mechanicId: Optional[int] = None
    bookingDate: datetime
    timeSlot: str
    status: Optional[str] = "PENDING"
    notes: Optional[str] = None

# --- Min / Flat Models (No Cycles) ---
class UserMin(UserBase):
    id: int
    role: str
    class Config:
        from_attributes = True

class VehicleMin(VehicleBase):
    id: int
    createdAt: datetime
    class Config:
        from_attributes = True

class BookingMin(BookingBase):
    id: int
    bookingCode: str
    vehicle: Optional[VehicleMin] = None
    user: Optional[UserMin] = None
    class Config:
        from_attributes = True

class MechanicMin(MechanicBase):
    id: int
    class Config:
        from_attributes = True

class ServiceMin(ServiceBase):
    id: int
    class Config:
        from_attributes = True

class SparepartMin(SparepartBase):
    id: int
    class Config:
        from_attributes = True

class InvoiceMin(BaseModel):
    id: int
    invoiceNumber: str
    totalCost: float
    grandTotal: float
    class Config:
        from_attributes = True

# --- Create Models ---
class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ServiceCreate(ServiceBase):
    pass

class MechanicCreate(MechanicBase):
    pass

class SparepartCreate(SparepartBase):
    pass

class VehicleCreate(VehicleBase):
    pass

class BookingCreate(BookingBase):
    serviceIds: List[int] = []

class ServiceLogBase(BaseModel):
    bookingId: int
    mechanicId: int
    sparepartId: Optional[int] = None
    description: str
    sparepartQty: Optional[int] = 0
    status: Optional[str] = "STARTED"

class ServiceLogCreate(ServiceLogBase):
    pass

class InvoiceBase(BaseModel):
    bookingId: int
    paymentStatus: Optional[str] = "UNPAID"
    paymentMethod: Optional[str] = None

class InvoiceCreate(BaseModel):
    bookingId: int

# --- Full Models (With Nested Relationships) ---

class ServiceLog(ServiceLogBase):
    id: int
    logDate: datetime
    mechanic: Optional[MechanicMin] = None
    sparepart: Optional[SparepartMin] = None
    class Config:
        from_attributes = True

class BookingServiceBase(BaseModel):
    bookingId: int
    serviceId: int
    priceAtBooking: float
    quantity: Optional[int] = 1

class BookingService(BookingServiceBase):
    id: int
    service: Optional[ServiceMin] = None
    class Config:
        from_attributes = True

class Booking(BookingBase):
    id: int
    bookingCode: str
    createdAt: datetime
    updatedAt: datetime
    user: Optional[UserMin] = None
    vehicle: Optional[VehicleMin] = None
    mechanic: Optional[MechanicMin] = None
    bookingServices: List[BookingService] = []
    serviceLogs: List[ServiceLog] = []
    invoice: Optional[InvoiceMin] = None
    class Config:
        from_attributes = True

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
    booking: Optional[BookingMin] = None
    class Config:
        from_attributes = True

class Vehicle(VehicleBase):
    id: int
    createdAt: datetime
    user: Optional[UserMin] = None
    class Config:
        from_attributes = True

class Service(ServiceBase):
    id: int
    class Config:
        from_attributes = True

class Mechanic(MechanicBase):
    id: int
    createdAt: datetime
    class Config:
        from_attributes = True

class Sparepart(SparepartBase):
    id: int
    class Config:
        from_attributes = True

class User(UserBase):
    id: int
    role: str
    createdAt: datetime
    vehicles: List[VehicleMin] = []
    bookings: List[BookingMin] = []
    class Config:
        from_attributes = True

