from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils.translation import gettext_lazy as _
from babel.dates import format_date

from .models import Arquivo, Transacao

class ArquivoForm(forms.ModelForm):
    class Meta:
        model = Arquivo
        fields = ['arquivo']
        widgets = {
            'arquivo': forms.FileInput(attrs={'class': 'file-input'})
        }

    def clean(self):
        arquivo = self.cleaned_data.get('arquivo')
        
        if not arquivo:
            raise ValidationError(_('O arquivo importado está vazio'))

        elif not (arquivo.name.endswith('.csv') or arquivo.name.endswith('.xml')):
            raise ValidationError(_('Formato de arquivo inválido.'))

        elif Arquivo.objects.filter(arquivo__exact='arquivos/' + arquivo.name).exists():
            raise ValidationError(_('Um arquivo para essa data já consta na base de dados'))


class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return format_date(obj['mes'], 'MMMM/yyyy', locale='pt_BR').title()


class AnaliseForm(forms.Form):
    query = Transacao.objects.annotate(mes=TruncMonth('data_hora')).values('mes').annotate(count=Count('mes')).order_by('mes').values('mes')

    data = MyModelChoiceField(label="Selecione o mês para analisar as transações", queryset=query)


