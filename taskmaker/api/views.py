from django.shortcuts import render
from rest_framework import generics, status
from .models import Tarefa
from .serializers import TarefaSerializer


class TarefasListCreate(generics.ListCreateAPIView):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
