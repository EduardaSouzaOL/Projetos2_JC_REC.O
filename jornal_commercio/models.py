from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify

class Noticia(models.Model):
    
    # Opções de categoria, baseadas no seu home.html
    CATEGORIA_CHOICES = [
        ('MUNDO', 'Mundo'),
        ('SEGURANCA_VIARIA', 'Segurança Viária'),
        ('CIDADES', 'Cidades'), # Para 'DESCASO' e 'ALERTA'
        ('POLITICA', 'Política'), # Para 'CRECHES'
        ('GERAL', 'Geral'),
    ]

    titulo = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        verbose_name="Título da notícia" # Ajuste no verbose_name
    )
    
    # NOVO: Resumo para aparecer na home page
    resumo = models.TextField(
        verbose_name="Resumo (linha fina)",
        help_text="Um breve resumo da notícia que aparecerá na home page.",
        blank=True,
        null=True
    )

    conteudo = models.TextField(
        blank=False,
        null=False,
        verbose_name="Conteúdo da notícia"
    )

    # MELHORIA: Ligar ao usuário (jornalista) do Django
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Se o autor for deletado, a notícia não é
        null=True, # Permite notícias sem autor definido
        blank=True,
        verbose_name="Autor"
    )
    
    # NOVO: Campo de Categoria
    categoria = models.CharField(
        max_length=50,
        choices=CATEGORIA_CHOICES,
        default='GERAL',
        verbose_name="Categoria"
    )

    data_publicacao = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data de publicação"
    )

    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última atualização"
    )

    # MELHORIA: Campo Slug para URLs amigáveis
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        help_text="Usado para a URL da notícia. Deixe em branco para gerar automaticamente."
    )

    # MELHORIA: Descomentado e configurado
    imagem_principal = models.ImageField(
        upload_to='noticias_imagens/', # Define um subdiretório em 'media'
        blank=True, # Imagem pode ser opcional
        null=True,
        verbose_name="Imagem Principal"
    )

    class Meta:
        ordering = ['-data_publicacao'] # Ordena as notícias da mais nova para a mais antiga

    def __str__(self):
        return self.titulo # Mais limpo
    
    def save(self, *args, **kwargs):
        # Gerar slug automaticamente a partir do título se não existir
        if not self.slug:
            self.slug = slugify(self.titulo)
            # Garante que o slug seja único, adicionando um número se necessário
            original_slug = self.slug
            queryset = Noticia.objects.all().filter(slug__iexact=self.slug).exists()
            count = 1
            while queryset:
                self.slug = f"{original_slug}-{count}"
                count += 1
                queryset = Noticia.objects.all().filter(slug__iexact=self.slug).exists()
                
        super(Noticia, self).save(*args, **kwargs)


class Feedback(models.Model):
    nome = models.CharField(max_length=100, blank=True, null=True, help_text="Nome (opcional)")
    email = models.EmailField(blank=True, null=True, help_text="E-mail (opcional)")
    mensagem = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        ordering = ['-data_envio']

    def __str__(self):
        return f"Feedback de {self.nome or 'Anônimo'} em {self.data_envio.strftime('%d/%m/%Y')}"
