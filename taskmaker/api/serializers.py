from rest_framework import serializers
from .models import Tarefa


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefa
        fields = ["id", "title", "notes", "date", "time", "task_id"]
