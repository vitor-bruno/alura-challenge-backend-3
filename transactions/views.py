import csv
from datetime import datetime

from django.db import transaction
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import ArquivoForm
from .models import Transacao, Arquivo

def index(request):
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

            return HttpResponseRedirect('/')

    else:
        form = ArquivoForm()
    
    return render(request, 'index.html', {'form': form, 'importacoes': Arquivo.objects.all()})


def date_from_file_line(file, line):
    return file.splitlines()[line].split(',')[-1][:10]