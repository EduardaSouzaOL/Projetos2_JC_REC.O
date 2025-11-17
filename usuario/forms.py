from django import forms
from django.contrib.auth.models import User
from django.forms import DateInput 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Perfil, Interesse, AssinanteNewsletter


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='E-mail',
        widget=forms.TextInput(attrs={'placeholder': 'Digite aqui seu E-mail', 'id': 'id_username'})
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite aqui sua Senha', 'id': 'id_password'})
    )

class RegistroUsuarioForm(forms.Form):
    nome_completo = forms.CharField(
        label="Nome Completo",
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Digite aqui seu nome completo'})
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={'placeholder': 'Digite aqui seu e-mail'})
    )
    data_nascimento = forms.DateField(
        label="Data de Nascimento",
        widget=DateInput(attrs={'type': 'date', 'placeholder': 'dd/mm/aaaa'})
    )
    cidade = forms.CharField(
        label="Cidade",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Selecione'})
    )
    estado = forms.CharField(
        label="Estado",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Selecione'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está registrado.")
        return email

class RegistroSenhaForm(forms.Form):
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite aqui'})
    )
    confirme_a_senha = forms.CharField(
        label="Confirme a senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite aqui'})
    )

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirme_a_senha = cleaned_data.get("confirme_a_senha")
        if senha and confirme_a_senha and senha != confirme_a_senha:
            raise forms.ValidationError("As senhas não conferem.")
        return cleaned_data

    def clean_senha(self):
        senha = self.cleaned_data.get('senha')
        try:
            validate_password(senha)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        return senha


class RegistroFrequenciaForm(forms.Form):
    FREQUENCIA_CHOICES = [
        ('varias_vezes', 'Várias vezes ao dia'),
        ('uma_vez', 'Uma vez ao dia'),
        ('raramente', 'Raramente'),
        ('nunca', 'Nunca'),
    ]
    frequencia = forms.ChoiceField(
        label="Qual sua frequência quanto acompanhar as notícias da sua cidade/estado?",
        choices=FREQUENCIA_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )

class RegistroInteressesForm(forms.Form):
    INTERESSE_CHOICES = [
        ('politica', 'Política'),
        ('seguranca', 'Segurança'),
        ('saude', 'Saúde e Bem-Estar'),
        ('educacao', 'Educação'),
        ('esporte', 'Esporte'),
        ('entretenimento', 'Entretenimento'),
    ]

    interesses = forms.MultipleChoiceField(
        label="Escolha um ou mais assuntos do seu interesse",
        choices=INTERESSE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False 
    )

class InteressesForm(forms.ModelForm):
    """
    Formulário para o usuário selecionar seus interesses.
    """
    # Usamos ModelMultipleChoiceField com widget CheckboxSelectMultiple
    # Isso dirá ao Django para renderizar uma lista de checkboxes
    interesses = forms.ModelMultipleChoiceField(
        queryset=Interesse.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Perfil
        fields = ['interesses']
        
class AssinanteNewsletterForm(forms.ModelForm):
    class Meta:
        model = AssinanteNewsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Seu melhor e-mail...',
                'class': 'form-control-newsletter',
                'aria-label': 'Email para newsletter'
            })
        }
        labels = {
            'email': ""
        }