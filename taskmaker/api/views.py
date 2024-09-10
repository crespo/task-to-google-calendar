from django.shortcuts import render
from rest_framework import generics, filters
from .models import Tarefa
from .serializers import TarefaSerializer


class TarefaList(generics.ListAPIView):
    serializer_class = TarefaSerializer

    def get_queryset(self):
        start_date = self.kwargs.get("start_date")
        end_date = self.kwargs.get("end_date")

        return Tarefa.objects.filter(data__range=[start_date, end_date])


class TarefaListCreate(generics.ListCreateAPIView):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["titulo"]


class TarefaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    lookup_field = "pk"
