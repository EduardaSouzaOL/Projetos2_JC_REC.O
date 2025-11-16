from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('salvar-feedback', views.salvar_feedback, name='salvar_feedback'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('noticia/<slug:slug>/', views.detalhe_noticia, name='detalhe_noticia'),
    path('comunidades/', views.ComunidadeListView.as_view(), name='comunidades_lista'),
    path('comunidades/<int:pk>/', views.ComunidadeDetailView.as_view(), name='comunidade_detalhe'),
    path('publicacao/<int:pk>/curtir/', views.curtir_publicacao, name='curtir_publicacao'),
    path('publicacao/<int:pk>/salvar/', views.salvar_publicacao, name='salvar_publicacao'),
    path('publicacao/<int:pk>/comentar/', views.adicionar_comentario, name='adicionar_comentario'),
    path('comunidades/<int:pk>/toggle_membro/', views.toggle_membro, name='toggle_membro'),
]