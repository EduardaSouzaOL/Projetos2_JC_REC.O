from django.contrib import admin
from .models import Categoria, Noticia, Feedback
from django.utils.html import format_html # Para mostrar a imagem no admin

# CATEGORIA
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug')
    prepopulated_fields = {'slug': ('nome',)} # Gera o slug automaticamente

# 2. NOTÍCIA 
@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    # Campos exibidos na lista de notícias
    list_display = ('titulo', 'categoria', 'autor', 'data_publicacao', 'display_imagem_principal')
    
    # Filtros laterais
    list_filter = ('categoria', 'autor', 'data_publicacao')
    
    # Campos de pesquisa
    search_fields = ('titulo', 'subtitulo', 'conteudo')
    
    # Campos que serão preenchidos automaticamente com base em outros campos
    prepopulated_fields = {'slug': ('titulo',)} 

    # Edição de campos:
    fieldsets = (
        (None, {
            'fields': ('titulo', 'subtitulo', 'autor', 'categoria', 'imagem_principal', 'conteudo')
        }),
        ('Informações de URL e Data', {
            'fields': ('slug', 'data_publicacao'),
            'classes': ('collapse',), # Deixa esta seção recolhida por padrão
        }),
    )
    
    # Método auxiliar para exibir a imagem no painel de lista
    def display_imagem_principal(self, obj):
        if obj.imagem_principal:
            # Retorna uma tag HTML com a imagem em miniatura
            return format_html('<img src="{}" width="50" height="auto" />', obj.imagem_principal.url)
        return "Sem Imagem"
    
    display_imagem_principal.short_description = 'Capa'


# 3. ADMIN PARA FEEDBACK
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'data_envio', 'mensagem_curta')
    list_filter = ('data_envio',)
    search_fields = ('nome', 'email', 'mensagem')
    readonly_fields = ('data_envio',) # Não permite editar a data de envio

    def mensagem_curta(self, obj):
        # Limita a exibição da mensagem para a lista
        return obj.mensagem[:50] + '...' if len(obj.mensagem) > 50 else obj.mensagem
    mensagem_curta.short_description = 'Mensagem'