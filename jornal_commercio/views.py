from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from .forms import FeedbackForm
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
    """
    Esta view cuida da página que mostra UMA comunidade e seu feed.
    (A sua segunda imagem do frontend)
    """
    model = Comunidade  # 1. Modelo principal que esta view vai buscar
    
    # 2. Template que será usado para exibir a página
    template_name = 'jornal_commercio/comunidade_detalhe.html'
    
    # 3. Nome da variável no template (ex: 'comunidade')
    context_object_name = 'comunidade'
    
    # 4. Esta função mágica nos deixa adicionar MAIS DADOS (contexto)
    #    para o template, além da 'comunidade'
    def get_context_data(self, **kwargs):
        # Primeiro, pega o contexto padrão (que já inclui a 'comunidade')
        context = super().get_context_data(**kwargs)
        
        # Pega o objeto 'comunidade' que a view já buscou
        comunidade = self.get_object()
        
        # --- BUSCANDO DADOS ADICIONAIS ---

        # 1. Busca todas as publicações desta comunidade
        todas_as_publicacoes = Publicacao.objects.filter(comunidade=comunidade)

        # 2. Filtra os "Destaques" (baseado no seu layout)
        context['destaques'] = todas_as_publicacoes.filter(is_destaque=True).order_by('-data_publicacao')[:10]
        
        # 3. Pega o feed principal (publicações que NÃO são destaque)
        context['feed_publicacoes'] = todas_as_publicacoes.filter(is_destaque=False).order_by('-data_publicacao')
        
        # 4. Busca "Notícias/Serviços" (baseado no layout)
        #    Por agora, vamos pegar as 10 últimas notícias gerais do site
        context['noticias_servicos'] = Noticia.objects.all().order_by('-data_publicacao')[:10]
        
        # 5. Retorna o contexto completo para o template
        return context