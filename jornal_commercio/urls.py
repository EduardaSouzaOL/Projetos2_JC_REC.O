from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('salvar-feedback', views.salvar_feedback, name='salvar_feedback'),
]

