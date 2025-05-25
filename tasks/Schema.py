from datetime import date
from typing import Optional
from django_ninja import Schema

class TaskBaseSchema(Schema):
    title: str
    description:str = ""
    deadline: date
    status :str

class TaskCreateScema(TaskBaseSchema):
    pass

class TaskUpdateSchema(Schema):
    title : Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[str] = None
    status: Optional[str] = None

class taskSchems(TaskBaseSchema):
    id : int
    created_at :date
    overdue : bool
