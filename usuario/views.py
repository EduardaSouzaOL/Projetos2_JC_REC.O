from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistroUsuarioForm

# Create your views here.
def registrar(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Usuário criado com sucesso para {username}! Você já pode fazer login.')
            return redirect('login')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'usuario/registrar.html', {'form': form})

@login_required
def perfil(request):
    return render(request, 'usuario/perfil.html')
