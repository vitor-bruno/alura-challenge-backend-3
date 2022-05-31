from random import randint

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

def usuarios(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'usuarios/usuarios.html', {'usuarios' : User.objects.filter(is_superuser=False, is_active=True)})

def cadastro(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = [str(randint(0,9)) for _ in range(6)]
        senha = ''.join(senha)
        
        if not nome.strip():
            messages.error(request, 'O campo nome não pode ficar em branco')
            return redirect('cadastro')
        
        if not email.strip():
            messages.error(request, 'O campo e-mail não pode ficar em branco')
            return redirect('cadastro')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.is_active:
                messages.error(request, 'Email já cadastrado no sistema')
                return redirect('cadastro')
            else:
                user.is_active = True
                user.first_name = nome
                user.set_password(senha)
                user.save()

        else:
            user = User.objects.create_user(username=email, email=email, password=senha, first_name=nome)
            user.save()
        
        messages.success(request, 'Cadastro realizado com sucesso!')

        enviar_email(email, nome, senha)

        return redirect('index')

    return render(request, 'usuarios/cadastro.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        user = User.objects.get(email=email)
        
        if not email.strip() or not senha.strip():
            messages.error(request, 'Os campos email e senha não podem ficar em branco')
            return redirect('login')
        
        if user:
            if user.is_active:
                user = auth.authenticate(request, username=email, password=senha)
                
                if user is not None:
                    auth.login(request, user)
                    messages.success(request, 'Login realizado com sucesso')
                    return redirect('index')
                
                messages.error(request, 'Senha incorreta, tente novamente')
            
            else:
                messages.error(request, 'Usuário desativado, fale com um administrador para reativar sua conta')
                return redirect('login')
        
        else:
            messages.error(request, 'Usuário não cadastrado no sistema')
            return redirect('login')

    return render(request, 'usuarios/login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def deleta_usuario(request, usuario_id):
    usuario = get_object_or_404(User, pk=usuario_id)
    usuario.is_active = False
    usuario.save()
    return redirect('usuarios')

def edita_usuario(request, usuario_id):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'usuarios/editar_usuario.html', { 'usuario' : get_object_or_404(User, pk=usuario_id)})

def atualiza_usuario(request):
    if request.method == 'POST':
        id = request.POST['usuario_id']
        nome = request.POST['nome']
        email = request.POST['email']
        
        if not nome.strip():
            messages.error(request, 'O campo nome não pode ficar em branco')
            return redirect('atualiza_usuario')
        
        if not email.strip():
            messages.error(request, 'O campo e-mail não pode ficar em branco')
            return redirect('atualiza_usuario')

        user = User.objects.get(pk=id)
        user.first_name = nome

        if email != user.email:
            user.email = email
            user.username = email
            senha = [str(randint(0,9)) for _ in range(6)]
            senha = ''.join(senha)

            enviar_email(email, nome, senha)
        
        user.save()
        messages.success(request, 'Alterações realizadas com sucesso!')

        return redirect('usuarios')


def enviar_email(destinatario, nome, senha):
    subject = 'Sistema Alura de Transações Financeiras'
    message = f'''Olá {nome}, bem vinde ao sistema de análise de transações financeiras da Alura.\n\n
    Segue os dados de acesso ao sistema:\n
    Email: {destinatario}\n
    Senha: {senha}'''

    send_mail(subject, message, settings.EMAIL_HOST_USER, [destinatario])
