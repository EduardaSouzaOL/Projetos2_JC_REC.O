from .forms import FeedbackForm
from usuario.forms import AssinanteNewsletterForm
from .models import Edicao

def global_feedback_form(request):
    return {
        'global_feedback_form': FeedbackForm()
    }
    
def newsletter_form_context(request):
    return {
        'newsletter_form': AssinanteNewsletterForm()
    }

def edicao_do_dia(request):
    ultima_edicao = Edicao.objects.first()
    return {'edicao_dia': ultima_edicao}