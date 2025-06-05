from ninja import Router, Query
from .models import Task
from .schema import TaskSchema, TaskCreateSchema, TaskUpdateSchema
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from ninja.pagination import paginate, PageNumberPagination
from datetime import date
from typing import List, Optional

router = Router()

CACHE_KEY_PREFIX = "tasks_client_"

def cache_key(client_id: str):
    return f"{CACHE_KEY_PREFIX}{client_id}"

@router.get("/tasks", response=List[TaskSchema])
@paginate(PageNumberPagination)
def list_tasks(request,
               status: Optional[str] = Query(None, description="Filter by status"),
               due: Optional[str] = Query(None, description="Filter by deadline: 'overdue', 'due'"),
               client_id: str = Query(..., description="Client ID to get own tasks")):
 
    key = cache_key(client_id)
    tasks = cache.get(key)
    if not tasks:
        # Cache miss: query DB
        tasks = Task.objects.filter(client_id=client_id).order_by("deadline")
        cache.set(key, list(tasks), timeout=60)  # Cache for 60 seconds

    # Filter in-memory from cached tasks (convert QuerySet to list)
    filtered_tasks = tasks
    if status:
        filtered_tasks = [t for t in filtered_tasks if t.status == status]

    if due == "overdue":
        filtered_tasks = [t for t in filtered_tasks if t.deadline < date.today() and t.status == Task.STATUS_PENDING]
    elif due == "due":
        filtered_tasks = [t for t in filtered_tasks if t.deadline <= date.today()]

    return filtered_tasks


@router.get("/tasks/{task_id}", response=TaskSchema)
def get_task(request, task_id: int, client_id: str = Query(...)):
    task = get_object_or_404(Task, id=task_id, client_id=client_id)
    return task


@router.post("/tasks", response=TaskSchema)
def create_task(request, payload: TaskCreateSchema):
    task = Task.objects.create(**payload.dict())
    # Invalidate cache for this client
    cache.delete(cache_key(payload.client_id))
    return task


@router.put("/tasks/{task_id}", response=TaskSchema)
def update_task(request, task_id: int, payload: TaskUpdateSchema, client_id: str = Query(...)):
    task = get_object_or_404(Task, id=task_id, client_id=client_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(task, attr, value)
    task.save()
    cache.delete(cache_key(client_id))
    return task


@router.delete("/tasks/{task_id}")
def delete_task(request, task_id: int, client_id: str = Query(...)):
    task = get_object_or_404(Task, id=task_id, client_id=client_id)
    task.delete()
    cache.delete(cache_key(client_id))
    return {"success": True}
