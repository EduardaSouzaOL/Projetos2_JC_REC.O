from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse
# Importe os Modelos
from .models import Noticia, Categoria, Feedback 
# Importe o Formulário de Feedback (Assumindo que ele está em forms.py)
from .forms import FeedbackForm 
import json


# ------------------ VIEWS PRINCIPAIS ------------------

def home(request):
    """
    View para a página inicial (Home).
    Exibe o formulário de feedback e as últimas notícias.
    """
    form_feedback = FeedbackForm() 
    
    # Exemplo: Pega as 5 notícias mais recentes para a Home
    ultimas_noticias = Noticia.objects.all().order_by('-data_publicacao').select_related('categoria')[:5]

    context = {
        'form_feedback': form_feedback,
        'ultimas_noticias': ultimas_noticias,
    }
    
    # Garanta que o caminho do template esteja correto
    return render(request, "jornal_commercio/home.html", context) 


def salvar_feedback(request):
    """
    Processa o formulário de feedback via POST (geralmente AJAX).
    """
    if request.method == 'POST':
        form = FeedbackForm(request.POST) 
        
        if form.is_valid():
            form.save()
            # Retorna JSON para requisições AJAX
            return JsonResponse({'success': True, 'message': 'Feedback enviado com sucesso! Obrigado.'})
        else:
            # Retorna erros do formulário em JSON
            errors = json.loads(form.errors.as_json())
            return JsonResponse({'success': False, 'errors': errors})
    
    # Retorna erro para métodos não permitidos
    return JsonResponse({'success': False, 'message': 'Método inválido.'}, status=405)


# ------------------ VIEWS DE NOTÍCIAS  ------------------

def detalhe_noticia(request, categoria_slug, noticia_slug):
    """
    Exibe o detalhe da notícia, buscando pelo slug da Categoria e da Notícia.
    """
    # 1. Busca a Categoria para garantir que a URL esteja correta e a notícia exista
    categoria = get_object_or_404(Categoria, slug=categoria_slug)
    
    # 2. Busca a Notícia pelo slug E a categoria para maior precisão e segurança
    noticia = get_object_or_404(
        Noticia.objects.select_related('categoria'), 
        categoria=categoria,
        slug=noticia_slug
    )
    
    # 3. Lógica para Notícias Relacionadas (da mesma categoria, excluindo a atual)
    noticias_relacionadas = Noticia.objects.filter(
        categoria=noticia.categoria
    ).exclude(
        pk=noticia.pk
    ).order_by('-data_publicacao').select_related('categoria')[:2] 
    
    context = {
        'noticia': noticia,
        'noticias_relacionadas': noticias_relacionadas,
        'form_feedback': FeedbackForm(), # Opcional: Incluir o form de feedback também no detalhe
    }
    
    return render(request, 'jornal_commercio/detalhe_noticia.html', context)


def lista_noticias_por_categoria(request, categoria_slug):
    """
    Exibe a lista de notícias filtradas por uma Categoria específica.
    """
    categoria = get_object_or_404(Categoria, slug=categoria_slug)
    
    # Filtra todas as notícias desta categoria
    noticias = Noticia.objects.filter(
        categoria=categoria
    ).order_by('-data_publicacao').select_related('categoria')

    context = {
        'categoria_atual': categoria,
        'noticias': noticias,
    }

    # Você pode usar o mesmo template para a lista principal ou criar um específico
    return render(request, 'jornal_commercio/lista_noticias.html', context)


def lista_noticias_arquivo(request):
    """
    Exibe o arquivo com todas as notícias.
    """
    noticias = Noticia.objects.all().order_by('-data_publicacao').select_related('categoria')
    
    context = {
        'noticias': noticias,
        'categorias': Categoria.objects.all(), # Opcional: para um menu lateral
    }
    
    return render(request, 'jornal_commercio/lista_noticias.html', context)