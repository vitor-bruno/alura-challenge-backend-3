from django import forms
from .models import Arquivo
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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

        elif not arquivo.name.endswith('.csv'):
            raise ValidationError(_('Formato de arquivo inválido.'))