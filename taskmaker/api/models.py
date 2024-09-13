from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=100)
    notes = models.TextField(null=True, blank=True)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    task_id = models.CharField(max_length=100, blank=True)


class Event(models.Model):
    summary = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    event_id = models.CharField(max_length=100, blank=True)
