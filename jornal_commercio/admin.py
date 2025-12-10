from django.contrib import admin
from .models import (
    Noticia, Feedback, Comunidade, Publicacao, Comentario, HistoricoLeitura,
    Quiz, Pergunta, Opcao, TentativaQuiz, RespostaUsuario,Edicao
)

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'autor', 'data_publicacao')
    list_filter = ('categoria', 'autor')
    search_fields = ('titulo', 'resumo', 'conteudo')
    # Mantivemos sua configuração de slug automático
    prepopulated_fields = {'slug': ('titulo',)}

admin.site.register(Feedback)

@admin.register(Comunidade)
class ComunidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criador', 'categoria', 'data_criacao')
    search_fields = ('nome', 'descricao')
    list_filter = ('criador', 'data_criacao', 'categoria')
    filter_horizontal = ('membros',) 

class ComentarioInline(admin.TabularInline):
    model = Comentario
    fields = ('autor', 'conteudo', 'data_publicacao')
    readonly_fields = ('data_publicacao',)
    extra = 0 

@admin.register(Publicacao)
class PublicacaoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'autor', 'comunidade', 'data_publicacao', 'is_destaque')
    list_filter = ('comunidade', 'autor', 'is_destaque')
    search_fields = ('conteudo', 'autor__username', 'comunidade__nome')
    filter_horizontal = ('curtidas', 'salvo_por')
    inlines = [ComentarioInline]

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'publicacao', 'data_publicacao')
    list_filter = ('autor', 'data_publicacao')
    search_fields = ('conteudo', 'autor__username')

@admin.register(HistoricoLeitura)
class HistoricoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'noticia', 'lido_completo')
    list_filter = ('usuario', 'lido_completo')


class OpcaoInline(admin.TabularInline):
    model = Opcao
    extra = 4
    min_num = 2 

@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'quiz', 'ordem')
    list_filter = ('quiz',)
    inlines = [OpcaoInline]
    search_fields = ('texto',)

class PerguntaInline(admin.StackedInline):
    model = Pergunta
    extra = 0
    show_change_link = True
    fields = ('texto', 'ordem')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('noticia', 'gerado_por_ia', 'data_criacao')
    inlines = [PerguntaInline]
    search_fields = ('noticia__titulo',)

class RespostaUsuarioInline(admin.TabularInline):
    model = RespostaUsuario
    extra = 0
    readonly_fields = ('pergunta', 'opcao_escolhida', 'data_resposta')
    can_delete = False
    
    def has_add_permission(self, request, obj):
        return False

@admin.register(TentativaQuiz)
class TentativaQuizAdmin(admin.ModelAdmin):

    list_display = ('usuario', 'quiz', 'pontuacao', 'concluido', 'data_inicio')
    list_filter = ('concluido', 'data_inicio', 'quiz')
    search_fields = ('usuario__username', 'quiz__noticia__titulo')
    inlines = [RespostaUsuarioInline]
    readonly_fields = ('data_inicio', 'data_conclusao', 'pontuacao')

@admin.register(Edicao)
class EdicaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_publicacao')
    ordering = ('-data_publicacao',)