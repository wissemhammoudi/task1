from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from modelORM import Person, PersonBase, Location, LocationBase
from databaseORM import db_dependency
from sqlalchemy import select,delete, func
router = APIRouter(prefix="/userORM", tags=["UsersORM"])
@router.post("/add",status_code=status.HTTP_201_CREATED)
def insert_user(person: PersonBase, location: LocationBase, db: db_dependency):
    try:
        # Create Location instance (in transient state)
        location_instance = Location(
            address=location.address,
            city=location.city
        )
        existing_location = db.query(Location).filter_by(address=location.address, city=location.city).first()
        if existing_location:
            raise HTTPException(status_code=409, detail="Location already exists")

        # Add location to the session
        db.add(location_instance)

        db.commit()  # Commit the location to the database to get its primary key
        existing_person = db.query(Person).filter_by(username=person.username).first()
        if existing_person:
            raise HTTPException(status_code=409, detail="Username already taken")
        # Create Person instance, linking it with the Location
        person_instance = Person(
            username=person.username,
            email_address=person.email_address,
            location_id=location_instance.location_id  # Use the location's ID
        )
        
        # Add person to the session
        db.add(person_instance)
        db.commit()  # Commit the person to the database
        
        return {"message": "User created successfully"}, status.HTTP_201_CREATED

    except IntegrityError:
        db.rollback()
        db.rollback()  # Rollback if there's a unique constraint violation or invalid data
        raise HTTPException(status_code=400, detail="Integrity constraint violated")
    except SQLAlchemyError as e:
        db.rollback()
        db.rollback()  # Rollback for other database errors
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get('/emails')
def get_user_emails(db: db_dependency):
    try:
        results = db.query(Person.email_address).all()
        return [email[0] for email in results] 
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
@router.get('/')
def get_users(db: db_dependency):
    try:
        result = db.query(Person).join(Location).all()
        users = [{"person": person, "location": person.location} for person in result]
        return users
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/filter-emails/{filter_value}")
def filter_emails(filter_value: str, db: db_dependency):
    try:
        result = db.query(Person.email_address).filter(Person.email_address.like(f"%{filter_value}%"))
        return {"filtered_emails": [filtredemail[0] for filtredemail in result] }
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.delete("/delete-user/{id}")
def delete_user(id: int, db: db_dependency):
    try:
        person = db.get(Person,id)
        if not person:
            raise HTTPException(status_code=404, detail="Person not found")
        db.delete(person)
        db.commit()
        
        return {"message": f"User {id} deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/update-email/{id}")
def update_user_email(id: int, new_email: str, db: db_dependency):
    try:
        person = db.get(Person,id)
        if not person:
            raise HTTPException(status_code=404, detail="Person not found")
        person.email_address = new_email
        db.commit()
 
        return {"message": f"Email for user {id} updated successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
@router.get("/nbrperson")
def nbr_person_per_city(db: db_dependency):
    try:
        result = (
            db.query(Location.city, func.count(Person.id).label('person_count'))
            .join(Person, Person.location_id == Location.id)
            .group_by(Location.city)
            .all()
        )
        
        return {"filtered_city_count": {row[0]: row[1] for row in result}}
    
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")