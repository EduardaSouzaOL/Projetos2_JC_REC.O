from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class Interesse(models.Model):
    """
    Modelo para armazenar os tipos de interesse (ex: Esporte, Política).
    """
    nome = models.CharField(max_length=100, unique=True)
    # Vamos usar o nome para encontrar a imagem estática no template
    
    class Meta:
        verbose_name_plural = "Interesses"

    def __str__(self):
        return self.nome

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    localizacao = models.CharField(max_length=100, blank=True)
    website = models.URLField(max_length=200, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=100, blank=True)
    frequencia = models.CharField(max_length=50, blank=True)
    # interesses = models.JSONField(default=list, blank=True)
    interesses = models.ManyToManyField(Interesse, blank=True)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

    def __str__(self):
        return f'Perfil de {self.usuario.username}'

@receiver(post_save, sender=User)
def create_user_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def save_user_perfil(sender, instance, **kwargs):
    try:
        instance.perfil.save()
    except Perfil.DoesNotExist:
        Perfil.objects.create(usuario=instance)
        
class AssinanteNewsletter(models.Model):

    email = models.EmailField(
        unique=True, 
        verbose_name="E-mail"
    )
    
    is_active = models.BooleanField(
        default=True, 
        verbose_name="Inscrição Ativa"
    )
    
    unsubscribe_token = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        unique=True,
        help_text="Token para descadastro"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Data de Inscrição"
    )

    class Meta:
        verbose_name = "Assinante da Newsletter"
        verbose_name_plural = "Assinantes da Newsletter"
        ordering = ['-created_at']

    def __str__(self):
        return self.email