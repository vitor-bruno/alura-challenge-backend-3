from django.db import models


class Arquivo(models.Model):
    arquivo = models.FileField(upload_to='arquivos/')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em']

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.conta_origem} - {self.conta_destino}: {self.valor}'