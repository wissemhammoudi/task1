from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from modelORM import Person, PersonBase, Location, LocationBase
from databaseORM import db_dependency
from sqlalchemy.orm import Session
router = APIRouter(prefix="/userORM", tags=["UsersORM"])
@router.post("/add")
def insert_user(person: PersonBase, location: LocationBase, db: db_dependency):
    try:
        # Create Location instance (in transient state)
        location_instance = Location(
            address=location.address,
            city=location.city
        )
        
        # Add location to the session
        db.add(location_instance)
        db.commit()  # Commit the location to the database to get its primary key
        
        # Create Person instance, linking it with the Location
        person_instance = Person(
            username=person.username,
            email_address=person.email_address,
            location_id=location_instance.location_id  # Use the location's ID
        )
        
        # Add person to the session
        db.add(person_instance)
        db.commit()  # Commit the person to the database
        
        return {"message": "User created successfully"}

    except IntegrityError:
        db.rollback()  # Rollback if there's a unique constraint violation or invalid data
        raise HTTPException(status_code=400, detail="User already exists or invalid data.")
    except SQLAlchemyError as e:
        db.rollback()  # Rollback for other database errors
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
