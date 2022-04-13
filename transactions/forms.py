from django import forms

class ArquivoForm(forms.Form):
    arquivo = forms.FileField()