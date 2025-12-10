from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timesince import timesince
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .forms import FeedbackForm, PublicacaoForm, ComentarioForm
import json
from .models import Noticia, Feedback, Comunidade, Publicacao, Comentario, Quiz, TentativaQuiz, RespostaUsuario, Opcao, Pergunta, HistoricoLeitura
from django.db.models import Q, Count, Sum
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST

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
    noticia = get_object_or_404(Noticia, slug=slug)

    todas_noticias = Noticia.objects.all()
    noticias_relacionadas = todas_noticias[1:4]
    
    comunidade_relacionada = Comunidade.objects.filter(categoria=noticia.categoria).first()
    
    respostas_ids = []
    quiz_concluido = False

    if request.user.is_authenticated and hasattr(noticia, 'quiz'):
        tentativa = TentativaQuiz.objects.filter(usuario=request.user, quiz=noticia.quiz).first()
        if tentativa:
            respostas_ids = list(tentativa.respostas.values_list('opcao_escolhida_id', flat=True))
            quiz_concluido = tentativa.concluido
            
    context = {
        'noticia': noticia,
        'noticias_relacionadas': noticias_relacionadas,
        'respostas_ids': respostas_ids,
        'quiz_concluido': quiz_concluido,
        'comunidade_relacionada': comunidade_relacionada,
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

class ComunidadeListView(ListView):
    model = Comunidade
    template_name = 'jornal_commercio/comunidades_lista.html'
    context_object_name = 'comunidades'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        filtro = self.request.GET.get('filtro', 'alta')
        
        categoria_filtro = self.request.GET.get('categoria')
        if categoria_filtro:
            queryset = queryset.filter(categoria=categoria_filtro)

        if filtro == 'seguindo' and self.request.user.is_authenticated:
            queryset = queryset.filter(membros=self.request.user)
        
        elif filtro == 'criados':
            queryset = queryset.order_by('-data_criacao')
        
        else:
            queryset = queryset.annotate(num_membros=Count('membros')).order_by('-num_membros')

        if query:
            queryset = queryset.filter(
                Q(nome__icontains=query) |
                Q(descricao__icontains=query)
            ).distinct()
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['filtro_ativo'] = self.request.GET.get('filtro', 'alta')
        context['categoria_ativa'] = self.request.GET.get('categoria', '') 
        from .models import CATEGORIA_CHOICES
        context['categorias'] = CATEGORIA_CHOICES
        return context

class ComunidadeDetailView(DetailView):
    model = Comunidade
    template_name = 'jornal_commercio/comunidade_detalhe.html'
    context_object_name = 'comunidade'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comunidade = self.get_object()
        
        noticia_id = self.request.GET.get('noticia_id')
        if noticia_id:
            try:
                context['noticia_referencia'] = Noticia.objects.get(id=noticia_id)
            except Noticia.DoesNotExist:
                context['noticia_referencia'] = None

        todas_as_publicacoes = Publicacao.objects.filter(comunidade=comunidade).order_by('-data_publicacao')
        
        context['destaques'] = todas_as_publicacoes.filter(is_destaque=True)[:10]
        context['feed_publicacoes'] = todas_as_publicacoes
        
        context['noticias_servicos'] = Noticia.objects.filter(
            categoria=comunidade.categoria
        ).order_by('-data_publicacao')[:10]
        
        context['form_publicacao'] = PublicacaoForm()
        
        context['form_comentario'] = ComentarioForm()
        
        return context

    def post(self, request, *args, **kwargs):
        comunidade = self.get_object()
        
        form = PublicacaoForm(request.POST)

        if form.is_valid():
            nova_publicacao = form.save(commit=False)
            
            nova_publicacao.comunidade = comunidade
            nova_publicacao.autor = request.user
            
            noticia_id = request.POST.get('noticia_id_hidden')
            if noticia_id:
                from .models import Noticia
                try:
                    noticia = Noticia.objects.get(id=noticia_id)
                    nova_publicacao.noticia_relacionada = noticia
                except:
                    pass
            
            nova_publicacao.save()
                        
            return redirect(request.path)  
        else:
            context = self.get_context_data()
            context['form_publicacao'] = form
            return self.render_to_response(context)
        
@login_required
def curtir_publicacao(request, pk):
    if request.method == 'POST':
        publicacao = get_object_or_404(Publicacao, pk=pk)
        user = request.user
        
        is_liked = False
        
        if user in publicacao.curtidas.all():
            publicacao.curtidas.remove(user)
            is_liked = False
        else:
            publicacao.curtidas.add(user)
            is_liked = True
            if user in publicacao.descurtidas.all():
                publicacao.descurtidas.remove(user)
            
        return JsonResponse({
            'success': True,
            'is_liked': is_liked,
            'likes_count': publicacao.curtidas.count(),
            'is_disliked': False,
            'dislikes_count': publicacao.descurtidas.count() 
        })
    else:
        return HttpResponseForbidden("Ação não permitida.")

@login_required
def descurtir_publicacao(request, pk):
    if request.method == 'POST':
        publicacao = get_object_or_404(Publicacao, pk=pk)
        user = request.user
        
        is_disliked = False
        
        if user in publicacao.descurtidas.all():
            publicacao.descurtidas.remove(user)
            is_disliked = False
        else:
            publicacao.descurtidas.add(user)
            is_disliked = True
            if user in publicacao.curtidas.all():
                publicacao.curtidas.remove(user)
            
        return JsonResponse({
            'success': True,
            'is_disliked': is_disliked,
            'dislikes_count': publicacao.descurtidas.count(),
            'is_liked': False,
            'likes_count': publicacao.curtidas.count() 
        })
    else:
        return HttpResponseForbidden("Ação não permitida.")
    
@login_required
def salvar_publicacao(request, pk):
    if request.method == 'POST':
        publicacao = get_object_or_404(Publicacao, pk=pk)
        user = request.user
        
        is_saved = False
        
        if user in publicacao.salvo_por.all():
            publicacao.salvo_por.remove(user)
            is_saved = False
        else:
            publicacao.salvo_por.add(user)
            is_saved = True
            
        return JsonResponse({
            'success': True,
            'is_saved': is_saved
        })
    
    else:
        return HttpResponseForbidden("Ação não permitida.")

@login_required
def adicionar_comentario(request, pk):
    if request.method == 'POST':
        publicacao = get_object_or_404(Publicacao, pk=pk)
        form = ComentarioForm(request.POST)
        
        if form.is_valid():
            novo_comentario = form.save(commit=False)
            novo_comentario.publicacao = publicacao
            novo_comentario.autor = request.user
            novo_comentario.save()
            
            return JsonResponse({
                'success': True,
                'autor': novo_comentario.autor.username,
                'conteudo': novo_comentario.conteudo,
                'data': timesince(novo_comentario.data_publicacao),
                'comments_count': publicacao.comentarios.count()
            })
        
        return JsonResponse({'success': False, 'error': 'Formulário inválido'})

    return HttpResponseForbidden("Ação não permitida.") 

@login_required
def toggle_membro(request, pk):
    if request.method == 'POST':
        comunidade = get_object_or_404(Comunidade, pk=pk)
        user = request.user
        
        is_member = False
        if user in comunidade.membros.all():
            comunidade.membros.remove(user)
            is_member = False
        else:
            comunidade.membros.add(user)
            is_member = True
            
        return JsonResponse({
            'success': True,
            'is_member': is_member,
            'membros_count': comunidade.membros.count()
        })
    else:
        return HttpResponseForbidden("Ação não permitida.")
    
def salvar_resposta_quiz(request):

    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.body)
        opcao_id = data.get('opcao_id')
        
        opcao = get_object_or_404(Opcao, id=opcao_id)
        quiz = opcao.pergunta.quiz

        tentativa, created = TentativaQuiz.objects.get_or_create(
            usuario=request.user, 
            quiz=quiz
        )
        
        RespostaUsuario.objects.get_or_create(
            tentativa=tentativa,
            pergunta=opcao.pergunta,
            defaults={'opcao_escolhida': opcao}
        )
        
        return JsonResponse({'status': 'ok', 'correta': opcao.correta})
    
    return JsonResponse({'status': 'erro', 'message': 'Não autorizado'}, status=403)

def finalizar_quiz(request, quiz_id):
    if request.method == "POST" and request.user.is_authenticated:
        tentativa = TentativaQuiz.objects.filter(usuario=request.user, quiz_id=quiz_id).first()
        
        if tentativa:
            tentativa.concluido = True
            tentativa.save()
            return JsonResponse({'status': 'ok', 'message': 'Quiz concluído!'})
            
    return JsonResponse({'status': 'erro'}, status=400)

def criar_admin_temporario(request):
    try:
        if User.objects.filter(username='admin').exists():
            return HttpResponse("O usuário 'admin' já existe! Tente logar.")
        
        User.objects.create_superuser('admin', 'admin@example.com', 'Admin12345!')
        
        return HttpResponse("<h1>SUCESSO!</h1><p>Usuário: <b>admin</b></p><p>Senha: <b>Admin12345!</b></p>")
    except Exception as e:
        return HttpResponse(f"<h1>ERRO:</h1> <p>{str(e)}</p>")

def quiz_hub(request):
    quizzes = Quiz.objects.all().order_by('-data_criacao')
    
    pontos_usuario = 0
    if request.user.is_authenticated:
        total = TentativaQuiz.objects.filter(usuario=request.user, concluido=True).aggregate(Sum('pontuacao'))
        pontos_usuario = total['pontuacao__sum'] or 0

    return render(request, 'jornal_commercio/quiz_hub.html', {
        'quizzes': quizzes,
        'pontos_usuario': pontos_usuario
    })

def quiz_play(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    
    respostas_ids = []
    quiz_concluido = False
    pontuacao = 0
    
    respostas_ids = []
    if request.user.is_authenticated:
        tentativa = TentativaQuiz.objects.filter(usuario=request.user, quiz=quiz).first()
        if tentativa:
            respostas_ids = list(tentativa.respostas.values_list('opcao_escolhida_id', flat=True))
            quiz_concluido = tentativa.concluido
            pontuacao = tentativa.pontuacao

    return render(request, 'jornal_commercio/quiz_play.html', {
        'quiz': quiz,
        'respostas_ids': respostas_ids,
        'quiz_concluido': quiz_concluido,
        'pontuacao_atual': pontuacao
    })

def pagina_edicao_do_dia(request):
    from .models import Edicao
    
    ultima_edicao = Edicao.objects.first()
    
    context = {
        'edicao': ultima_edicao
    }
    return render(request, 'edicao_do_dia.html', context)

@login_required
@require_POST
def atualizar_historico_leitura(request):
    try:
        data = json.loads(request.body)
        noticia_id = data.get('noticia_id')
        porcentagem = data.get('porcentagem')
        
        # Validação básica
        if not noticia_id or porcentagem is None:
            return JsonResponse({'status': 'erro', 'message': 'Dados inválidos'}, status=400)
            
        porcentagem = int(porcentagem)
        if porcentagem > 100: porcentagem = 100
        
        # Salva ou atualiza
        historico, created = HistoricoLeitura.objects.get_or_create(
            usuario=request.user,
            noticia_id=noticia_id
        )
        
        # Só atualizamos se a nova porcentagem for maior que a anterior
        # (para evitar que, ao subir a página, diminua o progresso)
        if porcentagem > historico.porcentagem_lida:
            historico.porcentagem_lida = porcentagem
            historico.save()
            
        return JsonResponse({'status': 'sucesso', 'lido': historico.lido_completo})
        
    except Exception as e:
        return JsonResponse({'status': 'erro', 'message': str(e)}, status=500)