from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Arquivo(models.Model):
    arquivo = models.FileField(upload_to='arquivos/')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    data_transacoes = models.DateField(null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-data_transacoes']


    def __str__(self):
        return self.arquivo.name


class Transacao(models.Model):
    arquivo = models.ForeignKey(Arquivo, on_delete=models.CASCADE)
    banco_origem = models.CharField(max_length=30, null=False, blank=False)
    agencia_origem = models.CharField(max_length=10, null=False, blank=False)
    conta_origem = models.CharField(max_length=20, null=False, blank=False)
    banco_destino = models.CharField(max_length=30, null=False, blank=False)
    agencia_destino = models.CharField(max_length=10, null=False, blank=False)
    conta_destino = models.CharField(max_length=20, null=False, blank=False)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    data_hora = models.DateTimeField(null=False, blank=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if Transacao.objects.filter(banco_origem__exact=self.banco_origem,
                                    agencia_origem__exact=self.agencia_origem,
                                    conta_origem__exact=self.conta_origem,
                                    banco_destino__exact=self.banco_destino,
                                    agencia_destino__exact=self.agencia_destino,
                                    conta_destino__exact=self.conta_destino,
                                    data_hora__year=self.data_hora.year,
                                    data_hora__month=self.data_hora.month,
                                    data_hora__day=self.data_hora.day).exists():
            raise ValidationError(_(f'Transação do banco {self.banco_origem}, agência {self.agencia_origem}, ' +
                                    f'conta {self.conta_origem} para o banco {self.banco_destino}, agência ' +
                                    f'{self.agencia_destino}, conta {self.conta_destino} já consta no banco de dados'))
        super(Transacao, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.conta_origem} - {self.conta_destino}: {self.valor}'