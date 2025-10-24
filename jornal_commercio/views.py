
from django.shortcuts import render

from django.http import JsonResponse
from .forms import FeedbackForm  
import json


def home(request):
    
    form_feedback = FeedbackForm() 

    context = {
        'form_feedback': form_feedback,
    }
    
    return render(request, "jornal_commercio/home.html", context) 


def salvar_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST) 
        
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Feedback enviado com sucesso! Obrigado.'})
        else:
            errors = json.loads(form.errors.as_json())
            return JsonResponse({'success': False, 'errors': errors})
    
    return JsonResponse({'success': False, 'message': 'Método inválido.'}, status=405)


from django.shortcuts import render, get_object_or_404
from .models import Noticia, Categoria # Importe os modelos

def detalhe_noticia(request, noticia_slug):
    # Usa get_object_or_404 para buscar a notícia pelo SLUG
    # Se não encontrar, retorna uma página 404
    noticia = get_object_or_404(Noticia.objects.select_related('categoria'), slug=noticia_slug)
    
    # Lógica para Notícias Relacionadas (da mesma categoria, excluindo a atual)
    noticias_relacionadas = Noticia.objects.filter(
        categoria=noticia.categoria
    ).exclude(
        pk=noticia.pk
    ).order_by('-data_publicacao')[:2] # Limita a 2, como no seu anexo
    
    context = {
        'noticia': noticia,
        'noticias_relacionadas': noticias_relacionadas,
    }
    
    # Renderiza o template que você criou (detalhe_noticia.html)
    return render(request, 'seu_app/detalhe_noticia.html', context)
