from django.db import models


class Tarefa(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(null=True, blank=True)
    data = models.DateField()
    horario = models.TimeField(null=True, blank=True)
    task_id = models.CharField(max_length=100)

    # def __str__(self):
    #     return self.data.strftime("%Y-%m-%d") + "T"
