from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import insert, select, delete, update, text, func
from models import person_table, PersonBase, location_table, LocationBase
from database import db_dependency_core

router = APIRouter(prefix="/user", tags=["Users"])

@router.post("/add",status_code=status.HTTP_201_CREATED)
def insert_user(person: PersonBase, location: LocationBase, db: db_dependency_core):
    try:
        location_insert = insert(location_table).values(
            address=location.address,
            city=location.city,
        )
        location_result = db.execute(location_insert)
        db.commit()
        
        location_id = location_result.inserted_primary_key[0]
        
        person_insert = insert(person_table).values(
            username=person.username,
            email_address=person.email_address,
            location_id=location_id
        )
        db.execute(person_insert)
        db.commit()
        
        return {"message": "User created successfully"}
    except IntegrityError:
        db.rollback()
        db.rollback()
        raise HTTPException(status_code=400, detail="Integrity constraint violated")
    except SQLAlchemyError as e:
        db.rollback()
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get('/')
def get_users(db: db_dependency_core):
    try:
        results = db.execute(text("""
            SELECT person.person_id, person.username, person.email_address, 
                   location.address, location.city
            FROM person
            JOIN location ON person.location_id = location.location_id
        """)).fetchall()
        
        users = [
            {"person_id": row[0], "username": row[1], "email_address": row[2], "address": row[3], "city": row[4]}
            for row in results
        ]
        return users
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get('/emails')
def get_user_emails(db: db_dependency_core):
    try:
        s = select(person_table.c.email_address)
        results = db.execute(s).fetchall()
        return [row[0] for row in results]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/filter-emails/{filter_value}")
def filter_emails(filter_value: str, db: db_dependency_core):
    try:
        s = select(person_table.c.email_address).where(person_table.c.email_address.like(f"%{filter_value}%"))
        result = db.execute(s).fetchall()
        return {"filtered_emails": [row[0] for row in result]}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.delete("/delete-user/{username}")
def delete_user(username: str, db: db_dependency_core):
    try:
        d = delete(person_table).where(person_table.c.username == username)
        result = db.execute(d)
        db.commit()
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"message": f"User {username} deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/update-email/{username}")
def update_user_email(username: str, new_email: str, db: db_dependency_core):
    try:
        u = update(person_table).where(person_table.c.username == username).values(email_address=new_email)
        result = db.execute(u)
        db.commit()
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"message": f"Email for user {username} updated successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/nbrperson")
def nbr_person_per_city(db: db_dependency_core):
    try:
        s = select(
            location_table.c.city,
            func.count(person_table.c.person_id).label('person_count')
        ).select_from(
            person_table.join(location_table, person_table.c.location_id == location_table.c.location_id)
        ).group_by(location_table.c.city)
        
        result = db.execute(s).fetchall()
        return {"filtered_city_count": {row[0]: row[1] for row in result}}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
