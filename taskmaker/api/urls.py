from django.urls import path, re_path
from . import views

urlpatterns = [
    path("api/", views.TarefaView.as_view(), name="tarefa-list-create-view"),
    re_path(
        "api/(?P<start_date>\d{4}-\d{2}-\d{2})/(?P<end_date>\d{4}-\d{2}-\d{2})$",
        views.TarefaByDateRangeListView.as_view(),
        name="tarefa-by-date-range-list-view",
    ),
    path(
        "api/<int:pk>/",
        views.TarefaRetrieveUpdateDestroyView.as_view(),
        name="tarefa-retrieve-update-destroy-view",
    ),
]
