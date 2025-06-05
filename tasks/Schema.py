from datetime import date, datetime
from typing import Optional
from django_ninja import Schema

class TaskBaseSchema(Schema):
    title: str
    description: str = ""
    deadline: date
    status: str

class TaskCreateSchema(TaskBaseSchema):
    client_id: str  # required to simulate user

class TaskUpdateSchema(Schema):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[date] = None
    status: Optional[str] = None

class TaskSchema(TaskBaseSchema):
    id: int
    created_at: datetime
    overdue: bool

    @classmethod
    def from_orm(cls, task):
        # Override to calculate overdue dynamically
        obj = super().from_orm(task)
        obj.overdue = task.deadline < date.today() and task.status == task.STATUS_PENDING
        return obj

