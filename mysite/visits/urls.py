from django.urls import path

from . import views


app_name = "visits"


urlpatterns = [
    path("", views.index, name="index"),
    path("goals/", views.select_goals, name="select_goals"),
    path("plan/", views.plan, name="plan"),
    path(
        "plan/add/<int:booth_id>/",
        views.add_to_plan,
        name="add_to_plan",
    ),
    path(
        "plan/remove/<int:item_id>/",
        views.remove_from_plan,
        name="remove_from_plan",
    ),
    path(
        "plan/status/<int:item_id>/",
        views.update_status,
        name="update_status",
    ),
]
