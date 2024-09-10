from django.urls import path
from . import views

urlpatterns = [
    path("api/", views.TarefasListCreate.as_view(), name="tarefa-view-create"),
]
