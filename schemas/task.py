from typing import Optional
from pydantic import BaseModel


class Task(BaseModel):
    id: str
    title: str
    description: str
    completed: bool


class CreateTask(BaseModel):
    title: str
    description: str
    completed: bool


class UpdateTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
