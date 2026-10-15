from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("add/", views.add_task, name="add_task"),
    path("edit/<int:task_id>/", views.edit_task, name="edit_task"),
    path("tasks/<int:task_id>/toggle/", views.toggle_task, name="toggle_task"),
]
