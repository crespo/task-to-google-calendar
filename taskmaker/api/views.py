from django.shortcuts import render
from rest_framework import generics, status
from .models import Tarefa
from .serializers import TarefaSerializer


class TarefaListCreate(generics.ListCreateAPIView):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer


class TarefaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    lookup_field = "pk"
