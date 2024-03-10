from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status
import models
from models import Todos
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from routers import auth, todos

app = FastAPI()
app.include_router(router=auth.router)
app.include_router(router=todos.router)    