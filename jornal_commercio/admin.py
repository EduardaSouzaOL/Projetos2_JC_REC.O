from django.contrib import admin

# Register your models here.
from .models import Noticia
from .models import Feedback
from .models import Comunidade
from .models import Publicacao
from .models import Comentario

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    # Campos que aparecem na lista de notícias
    list_display = ('titulo', 'categoria', 'autor', 'data_publicacao')
    
    # Filtros que aparecem na barra lateral
    list_filter = ('categoria', 'autor')
    
    # Barra de pesquisa
    search_fields = ('titulo', 'resumo', 'conteudo')
    
    # Preenche o 'slug' automaticamente a partir do 'titulo' (muito útil!)
    prepopulated_fields = {'slug': ('titulo',)}

admin.site.register(Feedback)

@admin.register(Comunidade)
class ComunidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criador', 'data_criacao')
    search_fields = ('nome', 'descricao')
    list_filter = ('criador', 'data_criacao')
    
    # Melhora a interface de adicionar/remover membros
    # (Transforma a lista de seleção em uma caixa de "filtro" horizontal)
    filter_horizontal = ('membros',) 


# Esta classe 'inline' permite ver e editar Comentários
# DIRETAMENTE de dentro da página de uma Publicação. É muito útil!
class ComentarioInline(admin.TabularInline):
    model = Comentario
    fields = ('autor', 'conteudo', 'data_publicacao')
    readonly_fields = ('data_publicacao',) # Não deixa editar data automática
    extra = 0 # Não mostra campos extras para novos comentários por padrão


@admin.register(Publicacao)
class PublicacaoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'autor', 'comunidade', 'data_publicacao', 'is_destaque')
    list_filter = ('comunidade', 'autor', 'is_destaque')
    search_fields = ('conteudo', 'autor__username', 'comunidade__nome')
    
    # Melhora a interface para 'curtidas' e 'salvo_por'
    filter_horizontal = ('curtidas', 'salvo_por')
    
    # Adiciona o 'inline' de comentários na página da publicação
    inlines = [ComentarioInline]

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'publicacao', 'data_publicacao')
    list_filter = ('autor', 'data_publicacao')
    search_fields = ('conteudo', 'autor__username')