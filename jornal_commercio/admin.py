from django.contrib import admin
from .models import Noticia
from .models import Feedback
from .models import Comunidade
from .models import Publicacao
from .models import Comentario

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'autor', 'data_publicacao')
    list_filter = ('categoria', 'autor')
    search_fields = ('titulo', 'resumo', 'conteudo')
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