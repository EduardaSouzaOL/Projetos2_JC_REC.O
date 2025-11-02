from .forms import FeedbackForm

def global_feedback_form(request):
    """Disponibiliza o formulário de feedback em todos os templates."""
    return {
        'global_feedback_form': FeedbackForm()
    }