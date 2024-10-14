from rest_framework import serializers
from .models import Task, Event


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "user", "title", "notes", "date", "time", "task_id"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "user",
            "summary",
            "description",
            "date",
            "time_start",
            "time_end",
            "event_id",
        ]
