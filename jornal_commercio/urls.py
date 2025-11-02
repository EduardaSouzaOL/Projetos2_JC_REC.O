from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('salvar-feedback', views.salvar_feedback, name='salvar_feedback'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('noticia/<slug:slug>/', views.detalhe_noticia, name='detalhe_noticia'),
]

