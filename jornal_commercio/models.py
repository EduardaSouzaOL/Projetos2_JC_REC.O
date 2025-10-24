from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# --- NOVO MODELO: Categoria (Necessário para o cabeçalho "Política | NOTÍCIA") ---
class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        # Gera o slug automaticamente a partir do nome, se não for fornecido
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

# --- MODELO ATUALIZADO: Noticia ---
class Noticia(models.Model):
    
    # RELACIONAMENTO: Adiciona Categoria para o cabeçalho (ex: Política)
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.SET_NULL, # Mantém a notícia se a categoria for deletada
        null=True, 
        verbose_name="Categoria"
    )

    titulo = models.CharField(
        max_length=200,
        verbose_name="Titulo da notícia"
    )

    # NOVO CAMPO: Subtítulo (o "lead" ou resumo abaixo do título)
    subtitulo = models.CharField(
        max_length=500,
        verbose_name="Subtítulo/Lead",
        blank=True
    )

    conteudo = models.TextField(
        verbose_name="Conteúdo da notícia"
    )

    # RELACIONAMENTO MELHORADO: Usar User para autor (ideal para autenticação e Admin)
    # Se você não quer usar a tabela User do Django, use o CharField atual, mas adicione um model Autor
    autor = models.CharField(
        max_length=200,
        verbose_name="Autor"
    )

    # NOVO CAMPO: Slug para URLs amigáveis (ex: /noticia/projeto-cnh-social-aprovado/)
    slug = models.SlugField(
        max_length=250,
        unique=True,
        blank=True,
        verbose_name="Slug (URL Amigável)"
    )

    # IMAGEM: Ative o campo de imagem
    imagem_principal = models.ImageField(
        upload_to='noticias_imagens/', # Define uma pasta para as imagens
        verbose_name="Imagem Principal",
        blank=True,
        null=True
    )

    data_publicacao = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data de publicação"
    )

    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última atualização"
    )

    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"
        ordering = ['-data_publicacao'] # Ordena pela mais recente

    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        # Gera o slug automaticamente a partir do título, se não for fornecido
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

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




# from django.db import models
# from django.utils import timezone

# class Noticia(models.Model):
    
#     # Considerar uso de SlugField para URLs

#     titulo = models.CharField(
#         max_length=200,
#         blank=False,
#         null=False,
#         verbose_name="Titulo de noticia"
#     )

#     conteudo = models.TextField(
#         blank=False,
#         null=False,
#         verbose_name="Conteudo da noticia"
#     )

#     autor = models.CharField(
#         max_length=200,
#         blank=False,
#         null=False,
#         verbose_name="Autor"
#     )

#     data_publicacao = models.DateTimeField(
#         default=timezone.now,
#         verbose_name="Data de publicacao"
#     )

#     data_atualizacao = models.DateTimeField(
#         auto_now=True,
#         verbose_name="Ultima atualizacao"
#     )

#     """ imagem_principal = models.ImageField(
#         upload_to=''#
#     ) """

#     def __str__(self):
#         return f"{self.titulo} - {self.autor}"
    
