from fastapi import APIRouter
from fastapi import HTTPException
from models import Choice
from database import db_dependency

# Create router instance for choice-related endpoints
router = APIRouter(prefix="/choice",tags=["choice"])

@router.get("/{question_id}")
async def get_choices(question_id: int, db: db_dependency):
    """
    Get all choices for a specific question
    Args:
        question_id (int): ID of the question to get choices for
        db (Session): Database session dependency
    Returns:
        list: List of Choice objects associated with the question
    Raises:
        HTTPException: If no choices are found for the question
    """
    # Query database for choices matching the question_id
    result = db.query(Choice).filter(Choice.question_id == question_id).all()
    # Raise 404 if no choices found
    if not result:
        raise HTTPException(status_code=404, detail="Choise not found")
    return result