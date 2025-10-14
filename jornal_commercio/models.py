from django.db import models
from django.utils import timezone

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
