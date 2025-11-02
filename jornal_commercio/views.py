from django.shortcuts import render
from django.http import JsonResponse
from .forms import FeedbackForm  
import json
from .models import Noticia

def home(request):
    
    form_feedback = FeedbackForm()

    todas_noticias = Noticia.objects.all()

    destaque_principal = todas_noticias.first()

    destaques_secundarios = todas_noticias[1:5]

    context = {
        'form_feedback': form_feedback,
        'destaque_principal': destaque_principal, # <--- NOVO
        'destaques_secundarios': destaques_secundarios,
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

def newsletter(request):
    return render(request, "jornal_commercio/newsletter.html")