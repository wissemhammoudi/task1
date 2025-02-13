from sqlalchemy import String, ForeignKey
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# Pydantic model for Location
class LocationBase(BaseModel):
    address: str = Field(..., max_length=255)
    city: str = Field(..., max_length=100)

# Pydantic model for Person
class PersonBase(BaseModel):
    username: str = Field(..., max_length=15)
    email_address: EmailStr = Field(..., max_length=255)
    location_id: Optional[int] = None  

class Base(DeclarativeBase):
    pass

class Location(Base):
    __tablename__ = 'Location'
    location_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Relationship where one location can have many people
    people: Mapped[list["Person"]] = relationship("Person", back_populates="location")

    def __repr__(self) -> str:
        return f"Location(id={self.location_id!r}, address={self.address!r}, city={self.city!r})"

class Person(Base):
    __tablename__ = 'Person'
    person_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)
    email_address: Mapped[str] = mapped_column(String(255), nullable=False)
    location_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Location.location_id"), nullable=True)
    
    # Relationship where each person can have one location (or no location)
    location: Mapped[Optional["Location"]] = relationship("Location", back_populates="people")

    def __repr__(self) -> str:
        return f"Person(id={self.person_id!r}, username={self.username!r}, email_address={self.email_address!r})"
