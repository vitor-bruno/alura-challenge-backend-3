import csv
from datetime import datetime

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Sum, F, Value, Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ArquivoForm, AnaliseForm
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
            instance.usuario = request.user
            instance.save()
            messages.success(request, 'Arquivo salvo com sucesso!')

            for row in csv.reader(file.splitlines(), delimiter=','):
                if (not row) or (row[-1][:10] != main_date) or ('' in row):
                    continue
                
                try:
                    data_hora = datetime.strptime(row[7], '%Y-%m-%dT%H:%M:%S')

                    Transacao.objects.create(arquivo=instance, banco_origem=row[0].title(),
                                                agencia_origem=row[1], conta_origem=row[2],
                                                banco_destino=row[3].title(), agencia_destino=row[4],
                                                conta_destino=row[5], valor=float(row[6]), data_hora=data_hora)

                except ValidationError as e:
                    errors += 1

            if errors:
                messages.warning(request, f'{errors} transações já constam no banco de dados e foram ignoradas')

            return redirect('index')

    else:
        form = ArquivoForm()

    return render(request, 'transacoes/index.html', {'form': form})

def importacoes(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'transacoes/importacoes.html', {'importacoes': Arquivo.objects.all()})

def detalha_transacoes(request, importacao_id):
    if not request.user.is_authenticated:
        return redirect('login')

    contexto = {
        'transacoes' : Transacao.objects.filter(arquivo_id=importacao_id),
        'importacao' : get_object_or_404(Arquivo, pk=importacao_id)
        }

    return render(request, 'transacoes/transacoes.html', contexto)

def analise_transacoes(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        mes_selecionado = request.POST['data']
        transacoes_mes = Transacao.objects.annotate(mes=TruncMonth('data_hora')).filter(mes=mes_selecionado)

        contexto = {
            'transacoes' : transacoes_suspeitas(transacoes_mes),
            'contas' : contas_suspeitas(transacoes_mes),
            'agencias' : agencias_suspeitas(transacoes_mes),
            'form' : AnaliseForm(request.POST)
        }

        return render(request, 'transacoes/transacoes_suspeitas.html', contexto)
    
    return render(request, 'transacoes/transacoes_suspeitas.html', { 'form' : AnaliseForm() })


def date_from_file_line(file, line):
    return file.splitlines()[line].split(',')[-1][:10]

def transacoes_suspeitas(transacoes):
    return transacoes.filter(valor__gte=100000).order_by('-valor')

def contas_suspeitas(transacoes):
    contas_entrada = transacoes.values(banco=F('banco_destino'), agencia=F('agencia_destino'), conta=F('conta_destino')) \
        .annotate(soma=Sum('valor'), tipo=Value('Entrada')).filter(soma__gte=1000000)

    contas_saida = transacoes.values(banco=F('banco_origem'), agencia=F('agencia_origem'), conta=F('conta_origem')) \
        .annotate(soma=Sum('valor'), tipo=Value('Saída')).filter(soma__gte=1000000)

    return contas_entrada.union(contas_saida).order_by('-soma')

def agencias_suspeitas(transacoes):
    agencias_entrada = transacoes.values(banco=F('banco_destino'), agencia=F('agencia_destino')) \
        .annotate(soma=Sum('valor'), tipo=Value('Entrada')).filter(soma__gte=1000000000)
    
    agencias_saida = transacoes.values(banco=F('banco_origem'), agencia=F('agencia_origem')) \
        .annotate(soma=Sum('valor'), tipo=Value('Saída')).filter(soma__gte=1000000000)

    return agencias_entrada.union(agencias_saida).order_by('-soma')