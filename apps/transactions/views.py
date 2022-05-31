import csv
import xml.etree.ElementTree as ET
from datetime import datetime

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Sum, F, Value
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
            invalidas = 0
            
            if request.FILES['arquivo'].name.endswith('.csv'):
                salvar_transacoes_csv(request, form)

            else:
                salvar_transacoes_xml(request, form)

            

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
        mes_selecionado =  datetime(*eval(request.POST['data'].replace("'", "\"")[25:-1]))

        transacoes_mes = Transacao.objects.annotate(mes=TruncMonth('data_hora')).filter(mes=mes_selecionado)

        contexto = {
            'transacoes' : transacoes_suspeitas(transacoes_mes),
            'contas' : contas_suspeitas(transacoes_mes),
            'agencias' : agencias_suspeitas(transacoes_mes),
            'form' : AnaliseForm(request.POST)
        }

        return render(request, 'transacoes/transacoes_suspeitas.html', contexto)
    
    return render(request, 'transacoes/transacoes_suspeitas.html', { 'form' : AnaliseForm() })


def salvar_arquivo(request, form, data):
    instance = form.save(commit=False)
    instance.data_transacoes = data
    instance.usuario = request.user
    instance.save()
    messages.success(request, 'Arquivo salvo com sucesso!')
    return instance

def salvar_transacoes_csv(request, form):
    arquivo = request.FILES['arquivo'].read().decode('utf-8')
    primeira_data = arquivo.splitlines()[0].split(',')[-1][:10]
    invalidas = 0

    instance = salvar_arquivo(request, form, primeira_data)

    for transacao in csv.reader(arquivo.splitlines(), delimiter=','):
        if (not transacao) or (transacao[-1][:10] != primeira_data) or ('' in transacao):
            continue
        
        try:
            data_hora = datetime.strptime(transacao[7], '%Y-%m-%dT%H:%M:%S')

            Transacao.objects.create(arquivo=instance, banco_origem=transacao[0].title(),
                                        agencia_origem=transacao[1], conta_origem=transacao[2],
                                        banco_destino=transacao[3].title(), agencia_destino=transacao[4],
                                        conta_destino=transacao[5], valor=float(transacao[6]), data_hora=data_hora)

        except ValidationError:
            invalidas += 1

    if invalidas:
        messages.warning(request, f'{invalidas} transações já constam no banco de dados e foram ignoradas')

def salvar_transacoes_xml(request, form):
    arquivo = request.FILES['arquivo']
    transacoes = ET.parse(arquivo).getroot()
    primeira_data = transacoes[0][-1].text[:10]
    invalidas = 0
    
    instance = salvar_arquivo(request, form, primeira_data)

    for transacao in transacoes:
        if (not transacao) or (transacao[-1].text[:10] != primeira_data) or ('' in transacao):
            continue
        
        try:
            data_hora = datetime.strptime(transacao[-1].text, '%Y-%m-%dT%H:%M:%S')

            Transacao.objects.create(arquivo=instance, banco_origem=transacao[0][0].text.title(),
                                        agencia_origem=transacao[0][1].text, conta_origem=transacao[0][2].text,
                                        banco_destino=transacao[1][0].text.title(), agencia_destino=transacao[1][1].text,
                                        conta_destino=transacao[1][2].text, valor=float(transacao[2].text), data_hora=data_hora)

        except ValidationError:
            invalidas += 1
    
    if invalidas:
        messages.warning(request, f'{invalidas} transações já constam no banco de dados e foram ignoradas')


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