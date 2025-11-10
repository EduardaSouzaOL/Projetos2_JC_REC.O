from django import forms
from .models import Feedback, Publicacao, Comentario

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'

class PublicacaoForm(forms.ModelForm):
    class Meta:
        model = Publicacao
        
        # O usuário só precisa digitar o 'conteudo'.
        # 'autor' e 'comunidade' serão definidos na view.
        fields = ['conteudo'] 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona um placeholder e remove o "label"
        self.fields['conteudo'].widget.attrs.update({
            'placeholder': 'Escreva sua publicação...',
            'rows': 3 # Deixa a caixa de texto menor
        })
        self.fields['conteudo'].label = False

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        
        # O usuário só precisa digitar o 'conteudo'.
        # 'autor' e 'publicacao' serão definidos na view.
        fields = ['conteudo'] 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona um placeholder e remove o "label"
        self.fields['conteudo'].widget.attrs.update({
            'placeholder': 'Escreva seu comentário...',
            'rows': 2 # Caixa de texto com 2 linhas
        })
        self.fields['conteudo'].label = False