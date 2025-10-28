from django.contrib import admin

# Register your models here.
from .models import Noticia

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
