from django.db import models


class Tarefa(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(null=True, blank=True)
    data = models.DateField()
    horario = models.TimeField(null=True, blank=True)

    def __str__(self):
        return (
            "Título: "
            + self.titulo
            + "\nDescrição: "
            + self.descricao
            + "\nData: "
            + self.data
            + "\nHorário: "
            + self.horario
        )
