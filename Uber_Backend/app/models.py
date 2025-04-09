from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base

# user model representing users in the system
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

# driver model representing drivers available for rides

class Driver(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    car_model = Column(String)
    available = Column(Boolean, default=True)

# ride model representing ride requests and their statuses
class Ride(Base):
    __tablename__ = "ride"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id")) # use user ID
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable = True)
    status = Column(String, default= "requested")
    user = relationship("User")
    driver = relationship("Driver")