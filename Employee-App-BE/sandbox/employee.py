""""
from fastapi import APIRouter, Depends, HTTPException, Path
from models import Employee
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user

# Define an API router for handling Auth routes, we will see a section called auth in the docs
router = APIRouter(
    prefix="/employee",
    tags=["employee"]
)

# Define a dependency for database sessions
# The get_db function is a context manager, which means it cleans up the session after use
def get_db():
    db = SessionLocal() # -> creates a new session
    try:
        yield db # -> uses and returns the session
    finally:
        db.close() # -> closes the session

# Define a new type representing a database session, with the get_db function as a dependency
# This means whenever an instance of this type is requested, FastAPI will call get_db to create it
db_dependency = Annotated[Session, Depends(get_db)]

# Similarly, define a new type representing a user, with the get_current_user function as a dependency
user_dependency = Annotated[dict, Depends(get_current_user)]

# Define a Pydantic model for Todo requests
class EmployeeRequest(BaseModel):
    name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    position: str = Field(min_length=3)
    
# we add a schema_extra attribute to the model to provide an example of the model
# which will be displayed in the docs
    class Config:
        schema_extra = {
            'example': {
                'name': 'Max',
                'last_name': 'Specter',
                'position': 'CEO',
                
            }
        }

# Define a route for getting all your personal employee data as a logged in user

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    # If no user is authenticated, raise an HTTP 401 error
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid authentication credentials")
    # Otherwise, return all data for the current user
    return db.query(Employee).filter(Employee.owner_id == user.get("id")).all()
    # it will return all the data for the current user, because we are filtering by the owner_id which should be the user.get("id") from the database

@router.get("/employee/{employee_id}", status_code=status.HTTP_200_OK)
async def read_employee_by_id(user: user_dependency, db: db_dependency, employee_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid authentication credentials")
    # Query for the Todo with the provided id owned by the current user
    employee_model = db.query(Employee).filter(Employee.id == employee_id).filter(Employee.owner_id == user.get('id')).first()
    if employee_model is not None:
        return employee_model
    raise HTTPException(status_code=404, detail="Employee not found")


# this endpoint is necessary for the first registration of the user, every user should register itself 
@router.post("/employee", status_code=status.HTTP_201_CREATED)
async def create_employee(user: user_dependency, 
                           db: db_dependency, 
                           employee_request: EmployeeRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid authentication credentials")
    # Create a new Todo model from the request data and the current user's id
    todo_model = Employee(**employee_request.dict(), owner_id=user.get("id"))

    db.add(todo_model)
    db.commit()

# this endpoint is necessary for changing the own employee data, like postion, name, last_name or vacation days. 
@router.put("/employee/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_employee(user: user_dependency, db: db_dependency, 
                      employee_request: EmployeeRequest,
                      employee_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid authentication credentials")
    # Query for the Todo with the provided id owned by the current user
    employee_model = db.query(Employee).filter(Employee.id == employee_id).filter(Employee.owner_id == user.get('id')).first()
    if employee_model is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
     # Update the Todo model with the request data
    employee_model.name = employee_request.name
    employee_model.last_name = employee_request.last_name
    employee_model.position = employee_request.position

    # Add the updated Todo to the database session and commit the changes
    db.add(employee_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    # If no user is authenticated, raise an HTTP 401 error
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid authentication credentials")
    todo_model = db.query(Employee).filter(Employee.id == todo_id).filter(Employee.owner_id == user.get('id')).first()
    # If no such Todo exists, raise an HTTP 404 error
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.query(Employee).filter(Employee.id == todo_id).filter(Employee.owner_id == user.get('id')).delete()

    db.commit()

"""

