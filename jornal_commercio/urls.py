from django.urls import path
from . import views
# Importe as Views baseadas em classes que definimos no guia anterior
from .views import ListaNoticiasView, DetalheNoticiaView, ListaPorCategoriaView 


urlpatterns = [
    # Rotas existentes
    path('', views.home, name="home"), # Ex: '/'
    path('salvar-feedback', views.salvar_feedback, name='salvar_feedback'),
    
    # ------------------ ROTAS DE NOTÍCIAS ------------------
    
    # Lista de todas as notícias (Ex: /noticias/)
    # Se você quiser que a lista principal fique na home, você pode mudar o path de 'ListaNoticiasView' para ''
    # Aqui, vamos assumir que existe um prefixo 'noticias/' no urls.py principal do projeto.
    path('noticias/', ListaNoticiasView.as_view(), name='lista_noticias'),
    
    # Notícias por Categoria (Ex: /noticias/politica/)
    path('noticias/<slug:categoria_slug>/', ListaPorCategoriaView.as_view(), name='lista_por_categoria'),
    
    # Detalhe da Notícia (Ex: /noticias/politica/titulo-da-noticia-aqui/)
    path('noticias/<slug:categoria_slug>/<slug:slug>/', DetalheNoticiaView.as_view(), name='detalhe_noticia'),
]
