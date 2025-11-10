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

class Comunidade(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    
    # Chave estrangeira para o usuário que criou a comunidade
    # (Ex: "Autor: AmandaFigueiredo")
    criador = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, # Se o criador for deletado, a comunidade continua
        null=True, 
        related_name="comunidades_criadas"
    )
    
    # Armazena todos os usuários que "seguem" esta comunidade
    # (Ex: "Comunidade Assinada" e "500K Membros")
    membros = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="comunidades_seguidas",
        blank=True
    )
    
    # As imagens vistas no front-end
    imagem_banner = models.ImageField(upload_to='banners_comunidade/', blank=True, null=True) # Imagem grande da pág. detalhe
    imagem_card = models.ImageField(upload_to='cards_comunidade/', blank=True, null=True)   # Imagem quadrada da lista
    
    data_criacao = models.DateTimeField(auto_now_add=True) # (Ex: "Desde 21 de agosto...")

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Comunidade"
        verbose_name_plural = "Comunidades"


class Publicacao(models.Model):

    comunidade = models.ForeignKey(
        Comunidade, 
        on_delete=models.CASCADE, # Se a comunidade for deletada, seus posts somem
        related_name="publicacoes" # Permite usar comunidade.publicacoes.all()
    )
    
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, # Se o autor for deletado, seus posts somem
        related_name="publicacoes"
    )
    
    # O conteúdo do post (ex: "Lorem ipsum...")
    conteudo = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    
    # Para a funcionalidade de "10 Destaques"
    is_destaque = models.BooleanField(default=False)

    # Armazena todos os usuários que curtiram este post
    # (Ex: "21K" curtidas)
    curtidas = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="publicacoes_curtidas",
        blank=True
    )

    # Armazena todos os usuários que salvaram este post
    salvo_por = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="publicacoes_salvas",
        blank=True
    )
    
    class Meta:
        ordering = ['-data_publicacao'] # Ordena os posts do mais novo para o mais antigo
        verbose_name = "Publicação"
        verbose_name_plural = "Publicações"

    def __str__(self):
        return f"Post de {self.autor.username} em {self.comunidade.nome}"


class Comentario(models.Model):

    publicacao = models.ForeignKey(
        Publicacao, 
        on_delete=models.CASCADE,
        related_name="comentarios" # Permite usar publicacao.comentarios.all()
    )
    
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="comentarios"
    )
    
    conteudo = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['data_publicacao'] # Ordena os comentários do mais antigo para o mais novo
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"

    def __str__(self):
        return f"Comentário de {self.autor.username} em {self.publicacao.id}"