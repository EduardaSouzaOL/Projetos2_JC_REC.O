from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('salvar-feedback', views.salvar_feedback, name='salvar_feedback'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('noticia/<slug:slug>/', views.detalhe_noticia, name='detalhe_noticia'),
    path('comunidades/', views.ComunidadeListView.as_view(), name='comunidades_lista'),
    path('comunidades/<int:pk>/', views.ComunidadeDetailView.as_view(), name='comunidade_detalhe'),
]

