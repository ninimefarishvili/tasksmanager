from ninja import Router
from .models import Task
from .Schemas import taskSchems, TaskCreateScema, TaskUpdateSchema
from django.shortcuts import get_object_or_404
import json
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from ninja.security import HttpBearer
from rest_framework_simplejwt.authentication import JWTAuthentication
from typing import List
from datetime import date
from django.core.cache import cache
from ninja.pagination import paginate, PageNumberPagination

router = Router()

@router.get("/tasks")
def get_books(request):
    Tasks = Task.objects.all()  
    return [taskSchems.from_orm(task) for task in Tasks]  
