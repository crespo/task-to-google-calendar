from django.shortcuts import render
from rest_framework import generics, filters, status
from .models import Tarefa
from .serializers import TarefaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .services.TaskManager import TaskManager, Task
from googleapiclient.errors import HttpError


class TarefaView(APIView):
    def get(self, request, format=None):
        search = request.query_params.get("search", "")

        if search:
            tarefas = Tarefa.objects.filter(titulo__icontains=search)
        else:
            tarefas = Tarefa.objects.all()

        serializer = TarefaSerializer(tarefas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        task = ""
        request_data = request.data
        errorOccurred = False

        if "titulo" in request_data and "data" in request_data:
            task = Task(
                request_data["titulo"],
                request_data["data"],
            )

            if "descricao" in request_data:
                task.descricao = request_data["descricao"]

            if "horario" in request_data:
                task.horario = request_data["horario"]

            createTaskResponse = TaskManager.createTask(task)

            if type(createTaskResponse) is HttpError:
                errorOccurred = True
            else:
                request_data["task_id"] = createTaskResponse["id"]

        serializer = TarefaSerializer(data=request_data)

        if serializer.is_valid():
            if not errorOccurred:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TarefaByDateRangeList(generics.ListAPIView):
    serializer_class = TarefaSerializer

    def get_queryset(self):
        start_date = self.kwargs.get("start_date")
        end_date = self.kwargs.get("end_date")

        return Tarefa.objects.filter(data__range=[start_date, end_date])


class TarefaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    lookup_field = "pk"
