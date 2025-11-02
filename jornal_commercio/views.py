from django.shortcuts import render
from django.http import JsonResponse
from .forms import FeedbackForm
import json
from .models import Noticia, Feedback 

def home(request):
    
    form_feedback = FeedbackForm()

    todas_noticias = Noticia.objects.all() 
    destaque_principal = todas_noticias.first()
    destaques_secundarios = todas_noticias[1:5]

    feedbacks_recentes = Feedback.objects.all().order_by('-id')[:5] 

    context = {
        'form_feedback': form_feedback,
        'destaque_principal': destaque_principal, 
        'destaques_secundarios': destaques_secundarios,
        'feedbacks': feedbacks_recentes, 
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