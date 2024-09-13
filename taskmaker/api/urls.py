from django.urls import path, re_path
from . import views

urlpatterns = [
    path("api/tasks/", views.TaskView.as_view(), name="task-list-create-view"),
    re_path(
        r"api/tasks/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})/$",
        views.TaskByDateRangeListView.as_view(),
        name="task-by-date-range-list-view",
    ),
    path(
        "api/tasks/<int:pk>/",
        views.TaskRetrieveUpdateDestroyView.as_view(),
        name="task-retrieve-update-destroy-view",
    ),
    path("api/events/", views.EventView.as_view(), name="event-list-create-view"),
    re_path(
        r"api/events/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})/$",
        views.EventByDateRangeListView.as_view(),
        name="event-by-date-range-list-view",
    ),
    path(
        "api/events/<int:pk>/",
        views.EventRetrieveUpdateDestroyView.as_view(),
        name="event-retrieve-update-destroy-view",
    ),
]
