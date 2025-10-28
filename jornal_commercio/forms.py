from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['nome', 'email', 'mensagem'] 
        
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Seu nome (opcional)', 
                'id': 'id_feedback_nome'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Seu e-mail (opcional)', 
                'id': 'id_feedback_email'
            }),
            'mensagem': forms.Textarea(attrs={
                'placeholder': 'Sua mensagem...', 
                'rows': 4, 
                'id': 'id_feedback_mensagem'
            }),
        }
        labels = {
            'nome': 'Nome',
            'email': 'E-mail',
            'mensagem': 'Mensagem',
        }