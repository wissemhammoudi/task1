from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from pydantic import BaseModel,Field ,EmailStr
from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
class Base(DeclarativeBase):
    pass
# Pydantic model for Location
class LocationBase(BaseModel):
    address: str = Field(..., max_length=255)
    city: str = Field(..., max_length=100)

# Pydantic model for Person
class PersonBase(BaseModel):
    username: str = Field(..., max_length=15)
    email_address: EmailStr = Field(..., max_length=255)
    location_id: Optional[LocationBase] = None  # Location ID will be optional for person creation


class Location(Base):
    __tablename__='Location'
    location_id= Column( Integer, primary_key=True, autoincrement=True),
    address= Column(String(255), nullable=False),
    city= Column(String(100), nullable=False),

class Person(Base):
    __tablename__='Person'
    person_id= Column( Integer, primary_key=True, autoincrement=True),
    username= Column( String(15), nullable=False, unique=True),
    email_address=Column( String(255), nullable=False),
    location_id=Column(Integer, nullable=True) 
    __table_args__=(
         ForeignKey(['location_id'],['Location.location_id'])
    )

