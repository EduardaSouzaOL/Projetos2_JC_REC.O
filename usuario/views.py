from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (
    RegistroUsuarioForm, 
    RegistroSenhaForm, 
    RegistroFrequenciaForm,
    RegistroInteressesForm,
    InteressesForm
)
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, update_session_auth_hash
from datetime import date 
from .models import Perfil, Interesse


def registrar(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            dados_passo_1 = form.cleaned_data
            dados_passo_1['data_nascimento'] = dados_passo_1['data_nascimento'].isoformat()
            request.session['registro_passo_1'] = dados_passo_1
            return redirect('registrar_senha') 
    else:
        form = RegistroUsuarioForm()
    return render(request, 'usuario/registrar.html', {'form': form})



def registrar_senha(request):
    dados_passo_1 = request.session.get('registro_passo_1')
    if not dados_passo_1:
        messages.error(request, 'Sessão expirada, por favor, comece novamente.')
        return redirect('registrar')
    if request.method == 'POST':
        form = RegistroSenhaForm(request.POST)
        if form.is_valid():
            request.session['registro_passo_2'] = form.cleaned_data
            return redirect('registrar_frequencia') 
    else:
        form = RegistroSenhaForm()
    return render(request, 'usuario/registrar_senha.html', {'form': form})


def registrar_frequencia(request):
    dados_passo_1 = request.session.get('registro_passo_1')
    dados_passo_2 = request.session.get('registro_passo_2')
    if not dados_passo_1 or not dados_passo_2:
        messages.error(request, 'Sessão expirada, por favor, comece novamente.')
        return redirect('registrar')
    if request.method == 'POST':
        form = RegistroFrequenciaForm(request.POST)
        if form.is_valid():
            request.session['registro_passo_3'] = form.cleaned_data
            return redirect('registrar_interesses') 
    else:
        form = RegistroFrequenciaForm()
    return render(request, 'usuario/registrar_frequencia.html', {'form': form})


def registrar_interesses(request):
    dados_passo_1_serializados = request.session.get('registro_passo_1')
    dados_passo_2 = request.session.get('registro_passo_2')
    dados_passo_3 = request.session.get('registro_passo_3')

    if not dados_passo_1_serializados or not dados_passo_2 or not dados_passo_3:
        messages.error(request, 'Sessão expirada, por favor, comece novamente.')
        return redirect('registrar')

    dados_passo_1 = dados_passo_1_serializados.copy()
    dados_passo_1['data_nascimento'] = date.fromisoformat(dados_passo_1['data_nascimento'])

    # --- INÍCIO DA CORREÇÃO (1/2) ---
    # Garante que os objetos Interesse existam no banco de dados ANTES de
    # o usuário tentar se registrar.
    # Usamos os Nomes (Labels) do seu formulário.
    nomes_interesses = [label for valor, label in RegistroInteressesForm.INTERESSE_CHOICES]
    for nome in nomes_interesses:
        Interesse.objects.get_or_create(nome=nome)
    # --- FIM DA CORREÇÃO (1/2) ---

    if request.method == 'POST':
        form = RegistroInteressesForm(request.POST)
        if form.is_valid():
            dados_passo_4 = form.cleaned_data

            try:
                email = dados_passo_1['email']
                nome_completo = dados_passo_1['nome_completo']
                senha = dados_passo_2['senha']
                first_name = nome_completo.split(' ', 1)[0]
                last_name = nome_completo.split(' ', 1)[-1] if ' ' in nome_completo else ''

                user = User.objects.create_user(
                    username=email, email=email, password=senha,
                    first_name=first_name, last_name=last_name
                )
                
                # O @receiver(post_save) já criou o user.perfil.
                # Agora atualizamos os campos dele.
                user.perfil.data_nascimento = dados_passo_1['data_nascimento']
                user.perfil.cidade = dados_passo_1['cidade']
                user.perfil.estado = dados_passo_1['estado']
                user.perfil.localizacao = f"{dados_passo_1['cidade']}, {dados_passo_1['estado']}"
                
                user.perfil.frequencia = dados_passo_3['frequencia']
                
                # Salvamos o perfil ANTES de lidar com o ManyToManyField
                user.perfil.save() 
                
                # --- INÍCIO DA CORREÇÃO (2/2) ---
                
                # 1. Pegue os valores (strings) selecionados (ex: ['politica', 'saude'])
                interesses_valores = dados_passo_4['interesses']

                # 2. Crie um mapa de valor -> nome (ex: 'politica' -> 'Política')
                mapa_interesses = dict(RegistroInteressesForm.INTERESSE_CHOICES)

                # 3. Converta os valores em nomes (ex: ['Política', 'Saúde'])
                nomes_para_buscar = [mapa_interesses[valor] for valor in interesses_valores if valor in mapa_interesses]
                
                # 4. Busque os OBJETOS Interesse no banco de dados
                interesses_obj = Interesse.objects.filter(nome__in=nomes_para_buscar)
                
                # 5. Adicione os objetos ao ManyToManyField usando .set()
                user.perfil.interesses.set(interesses_obj)
                
                # (A linha antiga "user.perfil.interesses = dados_passo_4['interesses']" foi removida)
                # (A linha antiga "user.perfil.save()" foi movida para cima)
                
                # --- FIM DA CORREÇÃO (2/2) ---
                
                del request.session['registro_passo_1']
                del request.session['registro_passo_2']
                del request.session['registro_passo_3']

                login(request, user)
                
                return redirect('registrar_sucesso') 

            except Exception as e:
                messages.error(request, f'Ocorreu um erro ao criar a conta: {e}')

    else:
        form = RegistroInteressesForm()
    
    return render(request, 'usuario/registrar_interesses.html', {'form': form})


@login_required 
def registrar_sucesso(request):
    return render(request, 'usuario/registrar_sucesso.html')

@login_required
def perfil(request):
    if request.method == 'POST':
        user = request.user
        
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.save()

        user.perfil.bio = request.POST.get('bio', '')
        user.perfil.localizacao = request.POST.get('localizacao', '')
        user.perfil.website = request.POST.get('website', '')
        user.perfil.save()
        
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil') 

    return render(request, 'usuario/perfil.html')

@login_required
def interesses(request):
    """
    View para o usuário gerenciar seus interesses.
    """
    # Garante que o perfil do usuário existe
    try:
        perfil = request.user.perfil
    except Perfil.DoesNotExist:
        perfil = Perfil.objects.create(user=request.user)

    # --- Opcional: Popular interesses no BD (só roda se não existirem) ---
    # Isso é útil para você não ter que cadastrá-los manualmente no admin
    # As imagens já existem na sua pasta static/usuario/images/interesses/
    nomes_interesses = ['Educação', 'Entretenimento', 'Esporte', 'Política', 'Saúde', 'Segurança']
    for nome in nomes_interesses:
        Interesse.objects.get_or_create(nome=nome)
    # --- Fim do trecho opcional ---

    if request.method == 'POST':
        # Salva os dados submetidos
        form = InteressesForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seus interesses foram atualizados com sucesso!')
            return redirect('interesses')
    else:
        # GET: Mostra o formulário com os interesses atuais do usuário marcados
        form = InteressesForm(instance=perfil)

    context = {
        'form': form
    }
    # Renderiza o template que você pediu
    return render(request, 'usuario/interesses.html', context)

@login_required
def privacidade(request):
    if request.method == 'POST':
        user = request.user
        
        email = request.POST.get('email')
        email_confirm = request.POST.get('email_confirm')
        
        telefone_ddd = request.POST.get('telefone_ddd', '')
        telefone_numero = request.POST.get('telefone_numero', '')
        
        senha_atual = request.POST.get('senha_atual')
        nova_senha = request.POST.get('nova_senha')
        confirmar_nova_senha = request.POST.get('confirmar_nova_senha')

        if email and email != user.email:
            if email != email_confirm:
                messages.error(request, 'Os e-mails não coincidem.')
                return redirect('privacidade')
            
            if User.objects.filter(email=email).exclude(pk=user.pk).exists():
                 messages.error(request, 'Este e-mail já está em uso.')
                 return redirect('privacidade')

            user.email = email
            user.username = email
            user.save()
            messages.success(request, 'E-mail atualizado com sucesso.')

        user.perfil.telefone = f"({telefone_ddd}) {telefone_numero}"
        user.perfil.save()
        
        if nova_senha and senha_atual:
            if not user.check_password(senha_atual):
                messages.error(request, 'A senha atual está incorreta.')
                return redirect('privacidade')
            
            if nova_senha != confirmar_nova_senha:
                messages.error(request, 'As novas senhas não coincidem.')
                return redirect('privacidade')
            
            user.set_password(nova_senha)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Senha atualizada com sucesso.')
            
        return redirect('privacidade')

    return render(request, 'usuario/privacidade.html')