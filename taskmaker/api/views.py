from django.http import Http404
from rest_framework import generics, status
from .models import Task
from .serializers import TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .services.TaskManager import TaskManager, TaskBuilder
from googleapiclient.errors import HttpError


class TaskView(APIView):
    def get(self, request, format=None):
        search = request.query_params.get("search", "")

        if search:
            tasks = Task.objects.filter(title__icontains=search)
        else:
            tasks = Task.objects.all()

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        task = ""
        request_data = request.data
        errorOccurred = False

        if "title" in request_data and "date" in request_data:
            task = TaskBuilder(
                request_data["title"],
                request_data["date"],
            )

            if "notes" in request_data:
                task.notes = request_data["notes"]

            if "time" in request_data:
                task.time = request_data["time"]

            createTaskResponse = TaskManager.createTask(task)

            if type(createTaskResponse) is HttpError:
                errorOccurred = True
            else:
                request_data["task_id"] = createTaskResponse["id"]

        serializer = TaskSerializer(data=request_data)

        if serializer.is_valid():
            if not errorOccurred:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskByDateRangeListView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        start_date = self.kwargs.get("start_date")
        end_date = self.kwargs.get("end_date")

        return Task.objects.filter(date__range=[start_date, end_date])


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = "pk"

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)

        return Response(serializer.data)

    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        TaskManager.deleteTask(task.task_id)
        task.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
