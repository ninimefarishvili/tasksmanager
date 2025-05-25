from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django_ninja import NinjaAPI

from tasks.api import router as TaskRouter
from tasks.api import auth_router as AuthRouter



def superuser_required(
    view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="/"
):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


api = NinjaAPI(
    csrf=False,
    docs_url="/docs",
    title="tasks API",
    docs_decorator=superuser_required,
    urls_namespace="api"
)


api.add_router("/app/", TaskRouter, tags=["tasks"])
api.add_router("/auth/", AuthRouter, tags=["Security"])
