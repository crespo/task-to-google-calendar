from django.shortcuts import render
from rest_framework import generics, filters
from .models import Tarefa
from .serializers import TarefaSerializer


class TarefaListCreate(generics.ListCreateAPIView):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["titulo"]


class TarefaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    lookup_field = "pk"
