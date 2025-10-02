from django.db import models
from django.utils import timezone


class Usuario(models.Model):
    nome_completo = models.CharField(
        max_length=200,
        verbose_name="Nome completo"
    )

    email = models.EmailField(
        max_length=50,
        unique=True,
        verbose_name="E-mail"
    )

    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Telefone"
    )

    data_nascimento = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de nascimento"
    )

    def __str__(self):
        return self.nome_completo or self.email

class Noticia(models.Model):
    
    # Considerar uso de SlugField para URLs

    titulo = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        verbose_name="Titulo de noticia"
    )

    conteudo = models.TextField(
        blank=False,
        null=False,
        verbose_name="Conteudo da noticia"
    )

    autor = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        verbose_name="Autor"
    )

    data_publicacao = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data de publicacao"
    )

    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Ultima atualizacao"
    )

    """ imagem_principal = models.ImageField(
        upload_to=''#
    ) """

    def __str__(self):
        return f"{self.titulo} - {self.autor}"
