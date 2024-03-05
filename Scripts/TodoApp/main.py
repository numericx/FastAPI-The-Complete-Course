from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status
import models
from models import Todos
from sqlalchemy.orm import Session
from database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = Session()
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool        

db_dependency = Annotated[Session, Depends(get_db)]

@app.get(path="/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()

@app.get(path="/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is not None:
        return todo_model
    else:
        raise HTTPException(status_code=404, detail="Todo not found.")
    
@app.post(path="/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo: TodoRequest):
    todo_model = Todos(**todo.dict())
    db.add(instance=todo_model)
    db.commit()

@app.put(path="/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo_by_id(db: db_dependency, 
                            todo: TodoRequest,
                            todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    else:
        todo_model.title = todo.title
        todo_model.description = todo.description
        todo_model.priority = todo.priority
        todo_model.complete = todo.complete

        db.add(instance=todo_model)
        db.commit()

@app.delete(path="/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    else:
        db.delete(instance=todo_model)
        db.commit()        