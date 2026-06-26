from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    role = Column(String(50), default="CUSTOMER")
    phone = Column(String(50), nullable=True)
    avatar = Column(String(255), nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    bookings = relationship("Booking", back_populates="user")
    vehicles = relationship("Vehicle", back_populates="user")

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    brand = Column(String(255))
    model = Column(String(255))
    year = Column(Integer)
    licensePlate = Column(String(255), unique=True, index=True)
    color = Column(String(50), nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="vehicles")
    bookings = relationship("Booking", back_populates="vehicle")

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    description = Column(String(500), nullable=True)
    category = Column(String(100), default="ROUTINE")
    price = Column(Float)
    estimatedMinutes = Column(Integer, default=60)
    isActive = Column(Boolean, default=True)

    bookingServices = relationship("BookingService", back_populates="service")

class Mechanic(Base):
    __tablename__ = "mechanics"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    phone = Column(String(50), nullable=True)
    specialization = Column(String(255), nullable=True)
    photo = Column(String(255), nullable=True)
    status = Column(String(50), default="AVAILABLE")
    createdAt = Column(DateTime, default=datetime.utcnow)

    bookings = relationship("Booking", back_populates="mechanic")
    serviceLogs = relationship("ServiceLog", back_populates="mechanic")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    bookingCode = Column(String(50), unique=True, index=True)
    userId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    vehicleId = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"))
    mechanicId = Column(Integer, ForeignKey("mechanics.id"), nullable=True)
    bookingDate = Column(DateTime)
    timeSlot = Column(String(50))
    status = Column(String(50), default="PENDING")
    notes = Column(String(500), nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="bookings")
    vehicle = relationship("Vehicle", back_populates="bookings")
    mechanic = relationship("Mechanic", back_populates="bookings")
    bookingServices = relationship("BookingService", back_populates="booking")
    serviceLogs = relationship("ServiceLog", back_populates="booking")
    invoice = relationship("Invoice", back_populates="booking", uselist=False)

class BookingService(Base):
    __tablename__ = "booking_services"
    id = Column(Integer, primary_key=True, index=True)
    bookingId = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"))
    serviceId = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"))
    priceAtBooking = Column(Float)
    quantity = Column(Integer, default=1)

    booking = relationship("Booking", back_populates="bookingServices")
    service = relationship("Service", back_populates="bookingServices")

class Sparepart(Base):
    __tablename__ = "spareparts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    partNumber = Column(String(100), unique=True, index=True)
    brand = Column(String(100), nullable=True)
    stock = Column(Integer, default=0)
    price = Column(Float)
    unit = Column(String(50), default="pcs")
    minStock = Column(Integer, default=5)

    serviceLogs = relationship("ServiceLog", back_populates="sparepart")

class ServiceLog(Base):
    __tablename__ = "service_logs"
    id = Column(Integer, primary_key=True, index=True)
    bookingId = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"))
    mechanicId = Column(Integer, ForeignKey("mechanics.id", ondelete="CASCADE"))
    sparepartId = Column(Integer, ForeignKey("spareparts.id"), nullable=True)
    description = Column(String(500))
    sparepartQty = Column(Integer, default=0)
    status = Column(String(50), default="STARTED")
    logDate = Column(DateTime, default=datetime.utcnow)

    booking = relationship("Booking", back_populates="serviceLogs")
    mechanic = relationship("Mechanic", back_populates="serviceLogs")
    sparepart = relationship("Sparepart", back_populates="serviceLogs")

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    invoiceNumber = Column(String(100), unique=True, index=True)
    bookingId = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"), unique=True)
    serviceCost = Column(Float, default=0)
    sparepartCost = Column(Float, default=0)
    totalCost = Column(Float, default=0)
    tax = Column(Float, default=0)
    grandTotal = Column(Float, default=0)
    paymentStatus = Column(String(50), default="UNPAID")
    paymentMethod = Column(String(50), nullable=True)
    paidAt = Column(DateTime, nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)

    booking = relationship("Booking", back_populates="invoice")
