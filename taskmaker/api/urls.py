from django.urls import path, re_path
from . import views

urlpatterns = [
    path("api/", views.TarefaView.as_view(), name="tarefa-view-list-create"),
    re_path(
        "api/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})$",
        views.TarefaByDateRangeList.as_view(),
        name="tarefa-by-date-range-view-list",
    ),
    path(
        "api/<int:pk>/",
        views.TarefaRetrieveUpdateDestroy.as_view(),
        name="tarefa-view-retrieve-update-destroy",
    ),
]
