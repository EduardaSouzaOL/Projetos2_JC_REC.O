from .forms import FeedbackForm
from usuario.forms import AssinanteNewsletterForm

def global_feedback_form(request):
    """Disponibiliza o formulário de feedback em todos os templates."""
    return {
        'global_feedback_form': FeedbackForm()
    }
    
def newsletter_form_context(request):
    return {
        'newsletter_form': AssinanteNewsletterForm()
    }