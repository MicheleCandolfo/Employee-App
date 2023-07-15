from fastapi import APIRouter, Depends, HTTPException, Path
from models import Users
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter(    
    prefix="/admin",
    tags=["admin"]
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# Define a Pydantic model for Todo requests
class UserRequest(BaseModel):
    #username: str = Field(min_length=3)
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    role: str = Field(min_length=3)



"""
@router.get("/employees", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Authentication credentials invalid")
    return db.query(Employee).all()
"""

@router.get("/users", status_code=status.HTTP_200_OK)
async def read_all_users(user: user_dependency, db: db_dependency):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Authentication credentials invalid")
    return db.query(Users).all()


@router.put("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(user: user_dependency, db: db_dependency, 
                      user_request: UserRequest,
                      user_id: int = Path(gt=0)):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid authentication credentials")
    # Query for the Todo with the provided id owned by the current user
    user_model = db.query(Users).filter(Users.id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    
     # Update the Todo model with the request data
    #user_model.username = user_request.username
    user_model.first_name = user_request.first_name
    user_model.last_name = user_request.last_name
    user_model.role = user_request.role

    # Add the updated Todo to the database session and commit the changes
    db.add(user_model)
    db.commit()


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: user_dependency, db: db_dependency, user_id: int = Path(gt=0)):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Authentication credentials invalid")
    users_model = db.query(Users).filter(Users.id == user_id).first()
    if users_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.query(Users).filter(Users.id == user_id).delete()
    db.commit()


