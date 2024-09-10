from django.urls import path
from . import views

urlpatterns = [
    path("api/", views.TarefaListCreate.as_view(), name="tarefa-view-list-create"),
    path(
        "api/<int:pk>/",
        views.TarefaRetrieveUpdateDestroy.as_view(),
        name="tarefa-view-retrieve-update-destroy",
    ),
]
