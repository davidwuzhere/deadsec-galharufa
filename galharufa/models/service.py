from datetime import datetime
from time import strftime
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid


class Servico(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    slug = models.SlugField(default="", db_index=True,
                            editable=False, unique=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    duracao = models.CharField(max_length=200)
    #imagem = models.ImageField(upload_to=f'static/images/servicos/')
    preco = models.FloatField()

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == "":
            self.slug = slugify(
                f'{self.titulo}-{datetime.now().strftime("%m%d%Y%H%M%S")}')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Serviço: {self.titulo} - Usuário: ({self.usuario})"

    class Meta:
        verbose_name_plural = "Serviços"
