from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.urls import reverse
from .forms import FeedbackForm, PublicacaoForm
import json
from .models import Noticia, Feedback, Comunidade, Publicacao, Comentario

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

def detalhe_noticia(request, slug):
    """
    Busca uma notícia específica pelo seu SLUG e a exibe na página de detalhe.
    """
    # Busca pelo campo 'slug' em vez de 'pk' (Primary Key)
    noticia = get_object_or_404(Noticia, slug=slug)

    todas_noticias = Noticia.objects.all()
    noticias_relacionadas = todas_noticias[1:4]

    
    context = {
        'noticia': noticia,
        'noticias_relacionadas': noticias_relacionadas,
    }
    
    return render(request, 'jornal_commercio/detalhe_noticia.html', context)

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

class ComunidadeListView(ListView):
    """
    Esta view cuida da página que lista TODAS as comunidades.
    (A sua primeira imagem do frontend)
    """
    model = Comunidade  # 1. Diz ao Django qual modelo buscar no banco
    
    # 2. Diz ao Django qual arquivo de template usar para exibir a página
    template_name = 'jornal_commercio/comunidades_lista.html'
    
    # 3. Dá um nome melhor para a lista no template
    # (Em vez do padrão 'object_list', usaremos 'comunidades')
    context_object_name = 'comunidades'
    
    # Opcional: para a paginação, se tiver muitas comunidades
    paginate_by = 10

class ComunidadeDetailView(DetailView):
    model = Comunidade
    template_name = 'jornal_commercio/comunidade_detalhe.html'
    context_object_name = 'comunidade'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comunidade = self.get_object()

        # Contexto que você já tinha:
        todas_as_publicacoes = Publicacao.objects.filter(comunidade=comunidade)
        context['destaques'] = todas_as_publicacoes.filter(is_destaque=True).order_by('-data_publicacao')[:10]
        context['feed_publicacoes'] = todas_as_publicacoes.filter(is_destaque=False).order_by('-data_publicacao')
        context['noticias_servicos'] = Noticia.objects.all().order_by('-data_publicacao')[:10]
        
        # --- NOVO ---
        # Adiciona o formulário de publicação ao contexto
        context['form_publicacao'] = PublicacaoForm()
        
        return context

    # --- MÉTODO NOVO PARA LIDAR COM POST ---
    def post(self, request, *args, **kwargs):
        # Pega a comunidade atual
        comunidade = self.get_object()
        
        # Cria uma instância do formulário com os dados do POST
        form = PublicacaoForm(request.POST)

        if form.is_valid():
            # Salva o formulário, mas não no banco ainda (commit=False)
            # Isso nos dá um objeto 'Publicacao' sem salvar
            nova_publicacao = form.save(commit=False)
            
            # Define os campos que faltam
            nova_publicacao.comunidade = comunidade
            nova_publicacao.autor = request.user # Pega o usuário logado
            
            # Agora sim, salva no banco
            nova_publicacao.save()
            
            # Redireciona para a mesma página (para evitar reenvio do form)
            # 'request.path' é a URL atual.
            return redirect(request.path)
        
        else:
            # Se o formulário for inválido, re-renderiza a página
            # Mas desta vez, o 'form' terá os erros
            context = self.get_context_data() # Pega todo o contexto de GET
            context['form_publicacao'] = form # Substitui o form vazio pelo form com erros
            return self.render_to_response(context)
        
@login_required # Garante que apenas usuários logados possam curtir
def curtir_publicacao(request, pk):
    """
    Esta view lida com a ação de curtir ou descurtir uma publicação.
    'pk' é o ID da Publicacao que está sendo curtida.
    """
    
    # Apenas permitimos requisições POST para esta ação
    if request.method == 'POST':
        # Busca a publicação pelo 'pk' ou retorna um erro 404
        publicacao = get_object_or_404(Publicacao, pk=pk)
        
        # Pega o usuário logado
        user = request.user
        
        # Verifica se o usuário já curtiu esta publicação
        if user in publicacao.curtidas.all():
            # Se sim, remove a curtida (descurtir)
            publicacao.curtidas.remove(user)
        else:
            # Se não, adiciona a curtida (curtir)
            publicacao.curtidas.add(user)
        
        # Redireciona o usuário de volta para a página da comunidade
        # O 'pk' aqui é da *comunidade*, para a qual a publicação pertence
        return redirect('comunidade_detalhe', pk=publicacao.comunidade.pk)
    
    else:
        # Se alguém tentar acessar esta URL via GET, retorna um erro
        return HttpResponseForbidden("Ação não permitida.")