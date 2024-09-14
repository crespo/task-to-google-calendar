from django.urls import path, re_path
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Task and Events to Google Calendar API",
        default_version="v1",
        description="This API helps managing tasks and events and integrates with Google Calendar API",
        terms_of_service="https://github.com/crespo/task-to-google-calendar/",
        contact=openapi.Contact(email="raulxcrespo@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("api/v1/tasks/", views.TaskView.as_view(), name="task-list-create-view"),
    re_path(
        r"api/v1/tasks/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})/$",
        views.TaskByDateRangeListView.as_view(),
        name="task-by-date-range-list-view",
    ),
    path(
        "api/v1/tasks/<int:pk>/",
        views.TaskRetrieveUpdateDestroyView.as_view(),
        name="task-retrieve-update-destroy-view",
    ),
    path("api/v1/events/", views.EventView.as_view(), name="event-list-create-view"),
    re_path(
        r"api/v1/events/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})/$",
        views.EventByDateRangeListView.as_view(),
        name="event-by-date-range-list-view",
    ),
    path(
        "api/v1/events/<int:pk>/",
        views.EventRetrieveUpdateDestroyView.as_view(),
        name="event-retrieve-update-destroy-view",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
