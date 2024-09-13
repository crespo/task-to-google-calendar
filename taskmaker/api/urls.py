from django.urls import path, re_path
from . import views

urlpatterns = [
    path("api/", views.TaskView.as_view(), name="task-list-create-view"),
    re_path(
        "api/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})$",
        views.TaskByDateRangeListView.as_view(),
        name="task-by-date-range-list-view",
    ),
    path(
        "api/<int:pk>/",
        views.TaskRetrieveUpdateDestroyView.as_view(),
        name="task-retrieve-update-destroy-view",
    ),
]
