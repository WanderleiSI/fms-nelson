from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.


class Categoria(models.Model):
    nome = models.CharField(max_length=250)
    user = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.nome


class Ganho(models.Model):
    descricao = models.TextField()
    valor = models.FloatField()
    data = models.DateField(default=now)
    user = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.descricao


class Despesas(models.Model):
    descricao = models.TextField()
    categoria = models.IntegerField(null=False, blank=False)
    valor = models.FloatField()
    data = models.DateField(default=now)
    user = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.descricao
