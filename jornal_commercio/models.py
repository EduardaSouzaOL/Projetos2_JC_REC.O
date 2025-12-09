from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.dispatch import receiver
import threading

CATEGORIA_CHOICES = [
    ('MUNDO', 'Mundo'),
    ('SEGURANCA_VIARIA', 'Segurança Viária'),
    ('CIDADES', 'Cidades'),
    ('POLITICA', 'Política'),
    ('GERAL', 'Geral'),
    ('EDUCACAO', 'Educação'),
    ('ESPORTE', 'Esporte'),
    ('SAUDE', 'Saúde e Bem-Estar'),
    ('MOBILIDADE', 'Mobilidade'),
    ('CULTURA', 'Cultura'),
    ('ENTRETENIMENTO', 'Entretenimento'),
    ('ECONOMIA', 'Economia'),
    ('COMERCIO', 'Comércio'),
    ('SOCIAL', 'Social'),
]

class Noticia(models.Model):
    
    titulo = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        verbose_name="Título da notícia"
    )
    
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

    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Autor"
    )
    
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

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        help_text="Usado para a URL da notícia. Deixe em branco para gerar automaticamente."
    )

    imagem_principal = models.ImageField(
        upload_to='noticias_imagens/',
        blank=True,
        null=True,
        verbose_name="Imagem Principal"
    )

    class Meta:
        ordering = ['-data_publicacao']

    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        try:
            return reverse('jornal_commercio:noticia_detalhe', kwargs={'slug': self.slug})
        except:
            return "/"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
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
    
    categoria = models.CharField(
        max_length=50,
        choices=CATEGORIA_CHOICES,
        default='GERAL',
        verbose_name="Categoria",
        unique=True
    )

    criador = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True, 
        related_name="comunidades_criadas"
    )
    
    membros = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="comunidades_seguidas",
        blank=True
    )
    
    imagem_banner = models.ImageField(upload_to='banners_comunidade/', blank=True, null=True)
    imagem_card = models.ImageField(upload_to='cards_comunidade/', blank=True, null=True)
    
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Comunidade"
        verbose_name_plural = "Comunidades"


class Publicacao(models.Model):

    comunidade = models.ForeignKey(
        Comunidade, 
        on_delete=models.CASCADE,
        related_name="publicacoes"
    )
    
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="publicacoes"
    )
    
    conteudo = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    
    is_destaque = models.BooleanField(default=False)

    curtidas = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="publicacoes_curtidas",
        blank=True
    )

    salvo_por = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="publicacoes_salvas",
        blank=True
    )
    
    noticia_relacionada = models.ForeignKey(
        Noticia,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="publicacoes_comunidade",
        verbose_name="Notícia Relacionada"
    )
    
    class Meta:
        ordering = ['-data_publicacao']
        verbose_name = "Publicação"
        verbose_name_plural = "Publicações"

    def __str__(self):
        return f"Post de {self.autor.username} em {self.comunidade.nome}"


class Comentario(models.Model):

    publicacao = models.ForeignKey(
        Publicacao, 
        on_delete=models.CASCADE,
        related_name="comentarios"
    )
    
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="comentarios"
    )
    
    conteudo = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['data_publicacao']
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"

    def __str__(self):
        return f"Comentário de {self.autor.username} em {self.publicacao.id}"
    

class HistoricoLeitura(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="historico_leitura"
    )
    
    noticia = models.ForeignKey(
        Noticia, 
        on_delete=models.CASCADE,
        related_name="leituras"
    )
    
    porcentagem_lida = models.PositiveIntegerField(
        default=0, 
        verbose_name="Porcentagem Lida"
    )
    
    lido_completo = models.BooleanField(default=False, verbose_name="Leitura Concluída")

    ultima_interacao = models.DateTimeField(auto_now=True) 

    class Meta:
        verbose_name = "Histórico de Leitura"
        verbose_name_plural = "Históricos de Leitura"
        unique_together = ('usuario', 'noticia')
        ordering = ['-ultima_interacao'] 

    def __str__(self):
        return f"{self.usuario} - {self.noticia} ({self.porcentagem_lida}%)"

    def save(self, *args, **kwargs):
        if self.porcentagem_lida >= 100:
            self.porcentagem_lida = 100
            self.lido_completo = True
        super(HistoricoLeitura, self).save(*args, **kwargs)

class Quiz(models.Model):
    noticia = models.OneToOneField(
        Noticia,
        on_delete=models.CASCADE,
        related_name='quiz',
        verbose_name="Notícia Relacionada"
    )
    titulo = models.CharField(max_length=200, verbose_name="Título do Quiz", blank=True)
    descricao = models.TextField(blank=True, verbose_name="Descrição/Instruções")
    
    gerado_por_ia = models.BooleanField(default=False, verbose_name="Gerado automaticamente?")
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quiz: {self.noticia.titulo}"

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"


class Pergunta(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='perguntas'
    )
    texto = models.TextField(verbose_name="Enunciado da Pergunta")
    ordem = models.PositiveIntegerField(default=0, help_text="Ordem de exibição")

    def __str__(self):
        return f"{self.quiz.noticia.titulo[:20]}... - {self.texto[:50]}"
    
    class Meta:
        ordering = ['ordem']


class Opcao(models.Model):

    pergunta = models.ForeignKey(
        Pergunta,
        on_delete=models.CASCADE,
        related_name='opcoes'
    )
    texto = models.CharField(max_length=255, verbose_name="Texto da Opção")
    correta = models.BooleanField(default=False, verbose_name="É a resposta correta?")

    def __str__(self):
        return f"({'X' if self.correta else ' '}) {self.texto}"

class TentativaQuiz(models.Model):

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tentativas_quiz'
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='tentativas'
    )
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)
    
    pontuacao = models.PositiveIntegerField(default=0, verbose_name="Acertos")
    
    concluido = models.BooleanField(default=False)

    class Meta:
        unique_together = ('usuario', 'quiz')
        verbose_name = "Tentativa de Quiz"
        verbose_name_plural = "Tentativas de Quiz"

    def __str__(self):
        status = "Concluído" if self.concluido else "Em andamento"
        return f"{self.usuario} - {self.quiz} ({status})"


class RespostaUsuario(models.Model):
    tentativa = models.ForeignKey(
        TentativaQuiz,
        on_delete=models.CASCADE,
        related_name='respostas'
    )
    pergunta = models.ForeignKey(
        Pergunta,
        on_delete=models.CASCADE
    )
    opcao_escolhida = models.ForeignKey(
        Opcao,
        on_delete=models.CASCADE
    )
    data_resposta = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tentativa', 'pergunta')

    def __str__(self):
        return f"Resposta de {self.tentativa.usuario} para {self.pergunta.id}"

@receiver(post_save, sender=Noticia)
def gerar_quiz_automatico(sender, instance, created, **kwargs):
    if created:
        print(f"--- GATILHO: Notícia '{instance.titulo}' criada. Iniciando geração de Quiz com IA... ---")
        
@receiver(post_save, sender=Noticia)
def gerar_quiz_automatico(sender, instance, created, **kwargs):

    if created:
        from .ai_service import gerar_quiz_com_gemini
        
        thread = threading.Thread(target=gerar_quiz_com_gemini, args=(instance,))
        thread.start()