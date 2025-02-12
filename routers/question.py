'''from fastapi import APIRouter
from fastapi import  HTTPException
from models import QuestionBase,Question,Choice,person_table,PersonBase
from database import db_dependency,db_dependency_core
from sqlalchemy import insert
# Create router instance for question-related endpoints
router = APIRouter( prefix="/question",tags=["questions"])

@router.get("/")
async def get_questions(db: db_dependency):
    try:
        result = db.query(Question).all()
        if not result:
            raise HTTPException(status_code=404, detail="No questions found")
        return result
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

@router.post("/")
async def create_question(question: QuestionBase, db: db_dependency):
    """
    Create a new question with associated choices
    Args:
        question (QuestionBase): Question data including choices
        db (Session): Database session dependency
    Returns:
        None
    """
    try:
        # Create new Question record
        db_question = Question(question_text=question.question_text)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        # Create Choice records for each choice in the question
        for choice in question.choices:
            db_choice = Choice(
                choice_text=choice.choice_text, 
                is_correct=choice.is_correct, 
                question_id=db_question.id
            )
            db.add(db_choice)
        db.commit()
        return {"message": "Question and choices created successfully"}
    
    except SQLAlchemyError as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

@router.get("/{question_text}")
async def get_question(question_text: str, db: db_dependency):
    """
    Get a specific question by text
    Args:
        question_text (str): Text of the question to search for
        db (Session): Database session dependency
    Returns:
        List[Question]: List of questions matching the search
    """
    try:
        result = db.query(Question).filter(Question.question_text.ilike(f"%{question_text}%")).limit(5).all()
        if not result:
            raise HTTPException(status_code=404, detail="Question not found")
        return result
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

@router.delete("/{question_id}")
async def delete_question(question_id: int, db: db_dependency):
    try:
        # Find the question by ID
        result = db.query(Question).filter(Question.id == question_id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Question not found")

        # Delete the associated choices
        choices = db.query(Choice).filter(Choice.question_id == question_id).all()
        for choice in choices:
            db.delete(choice)

        # Delete the question
        db.delete(result)
        db.commit()
        return {"message": "Question and associated choices deleted successfully"}
    
    except SQLAlchemyError as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

@router.patch("/{question_id}")
async def update_question(question_id: int, question: str, db: db_dependency):
    try:
        result = db.query(Question).filter(Question.id == question_id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Question not found")
        
        # Update the question text
        result.question_text = question
        db.commit()
        return {"message": "Question updated successfully"}
    
    except SQLAlchemyError as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
'''