import csv
from datetime import datetime
from random import randint
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ArquivoForm
from .models import Transacao, Arquivo

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        
        form = ArquivoForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES['arquivo'].read().decode('utf-8')
            main_date = date_from_file_line(file, 0)
            errors = 0

            instance = form.save(commit=False)
            instance.data_transacoes = main_date
            instance.save()
            messages.success(request, 'Arquivo salvo com sucesso!')

            for row in csv.reader(file.splitlines(), delimiter=','):
                if (not row) or (row[-1][:10] != main_date) or ('' in row):
                    continue
                
                try:
                    data_hora = datetime.strptime(row[7], '%Y-%m-%dT%H:%M:%S')

                    Transacao.objects.create(arquivo=instance, banco_origem=row[0],
                                                agencia_origem=row[1], conta_origem=row[2],
                                                banco_destino=row[3], agencia_destino=row[4],
                                                conta_destino=row[5], valor=float(row[6]), data_hora=data_hora)

                except ValidationError as e:
                    errors += 1

            if errors:
                messages.warning(request, f'{errors} transações já constam no banco de dados e foram ignoradas')

            return redirect('index')

    else:
        form = ArquivoForm()

    return render(request, 'index.html', {'form': form})

def importacoes(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'imports.html', {'importacoes': Arquivo.objects.all()})

def usuarios(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'usuarios.html', {'usuarios' : User.objects.filter(is_superuser=False)})

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
            messages.error(request, 'Email já cadastrado')
            return redirect('cadastro')

        user = User.objects.create_user(username=email, email=email, password=senha, first_name=nome)
        user.save()
        messages.success(request, 'Cadastro realizado com sucesso!')

        enviar_email(email, nome, senha)

        return redirect('index')

    return render(request, 'cadastro.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        
        if not email.strip() or not senha.strip():
            messages.error(request, 'Os campos email e senha não podem ficar em branco')
            return redirect('login')
        
        if User.objects.filter(email=email).exists():
            user = auth.authenticate(request, username=email, password=senha)
            
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Login realizado com sucesso')
                return redirect('index')
        
        else:
            messages.error(request, 'Usuário não cadastrado no sistema')
            return redirect('login')

    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def deleta_usuario(request, usuario_id):
    usuario = get_object_or_404(User, pk=usuario_id)
    usuario.delete()
    return redirect('usuarios')

def edita_usuario(request, usuario_id):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'editar_usuario.html', { 'usuario' : get_object_or_404(User, pk=usuario_id)})

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


def date_from_file_line(file, line):
    return file.splitlines()[line].split(',')[-1][:10]

def enviar_email(destinatario, nome, senha):
    subject = 'Sistema Alura de Transações Financeiras'
    message = f'''Olá {nome}, bem vinde ao sistema de análise de transações financeiras da Alura.\n\n
    Segue os dados de acesso ao sistema:\n
    Email: {destinatario}\n
    Senha: {senha}'''

    send_mail(subject, message, settings.EMAIL_HOST_USER, [destinatario])