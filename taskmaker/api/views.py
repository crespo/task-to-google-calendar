from django.http import Http404
from rest_framework import generics, status
from .models import Task, Event
from .serializers import TaskSerializer, EventSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .services.TaskManager import TaskManager, TaskBuilder
from .services.EventManager import EventManager, EventBuilder
from googleapiclient.errors import HttpError


class TaskView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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

            CREATE_TASK_RESPONSE = TaskManager.createTask(task)

            if type(CREATE_TASK_RESPONSE) is HttpError:
                errorOccurred = True
            else:
                request_data["task_id"] = CREATE_TASK_RESPONSE["id"]

        serializer = TaskSerializer(data=request_data)

        if serializer.is_valid():
            if not errorOccurred:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskByDateRangeListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = TaskSerializer

    def get_queryset(self):
        start_date = self.kwargs.get("start_date")
        end_date = self.kwargs.get("end_date")

        return Task.objects.filter(date__range=[start_date, end_date])


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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


class EventView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        search = request.query_params.get("search", "")

        if search:
            events = Event.objects.filter(summary__icontains=search)
        else:
            events = Event.objects.all()

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        event = ""
        request_data = request.data
        errorOccurred = False

        if "summary" in request_data and "date" in request_data:
            event = EventBuilder(
                request_data["summary"],
                request_data["date"],
            )

            if "description" in request_data:
                event.description = request_data["description"]

            if "time_start" in request_data and "time_end" in request_data:
                event.time_start = request_data["time_start"]
                event.time_end = request_data["time_end"]

            CREATE_EVENT_RESPONSE = EventManager.createEvent(event)

            if type(CREATE_EVENT_RESPONSE) is HttpError:
                errorOccurred = True
            else:
                request_data["event_id"] = CREATE_EVENT_RESPONSE["id"]

        request_data["user"] = request.user.id
        serializer = EventSerializer(data=request_data)

        if serializer.is_valid():
            if not errorOccurred:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventByDateRangeListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = EventSerializer

    def get_queryset(self):
        start_date = self.kwargs.get("start_date")
        end_date = self.kwargs.get("end_date")

        return Event.objects.filter(date__range=[start_date, end_date])


class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = "pk"

    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = EventSerializer(event)

        return Response(serializer.data)

    def put(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        EventManager.deleteEvent(event.event_id)
        event.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
