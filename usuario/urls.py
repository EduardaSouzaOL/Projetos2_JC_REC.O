# usuario/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomLoginForm 

urlpatterns = [
    path('registrar/', views.registrar, name='registrar'),
    
    path('login/', auth_views.LoginView.as_view(
        template_name='usuario/login.html',
        authentication_form=CustomLoginForm
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        template_name='usuario/logout.html'
    ), name='logout'),
    path('registrar/senha/', views.registrar_senha, name='registrar_senha'),
    path('registrar/frequencia/', views.registrar_frequencia, name='registrar_frequencia'),
    path('registrar/interesses/', views.registrar_interesses, name='registrar_interesses'),
    path('registrar/sucesso/', views.registrar_sucesso, name='registrar_sucesso'),
    path('perfil/', views.perfil, name='perfil'),
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='usuario/password_reset.html' 
         ), 
         name='password_reset'),

    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='usuario/password_reset_done.html' 
         ), 
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='usuario/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),

    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='usuario/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]