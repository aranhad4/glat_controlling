import random
import string
from django.db import models
from django.utils import timezone
from fornecedores.models import Fornecedor

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    ean = models.CharField(max_length=13, unique=True, blank=False, null=False)
    descricao = models.TextField(blank=True, null=True)
    quantidade = models.PositiveIntegerField(default=0)
    un_medida = models.CharField(max_length=10, blank=False, null=False)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, null=True, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    data_criacao = models.DateTimeField(default=timezone.now) 
    data_atualizacao = models.DateTimeField(auto_now=True)
    foto = models.ImageField(upload_to='produtos/', blank=True, null=True)
    codigo = models.CharField(max_length=10, unique=True, blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    def gerar_codigo(self):
        """Gera um código aleatório de 10 caracteres, composto por letras e números"""
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        return codigo

    def save(self, *args, **kwargs):
        """Override do método save para gerar o código antes de salvar o produto"""
        if not self.codigo:
            self.codigo = self.gerar_codigo()
        super().save(*args, **kwargs)


class HistoricoProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    campo = models.CharField(max_length=255)
    valor_antigo = models.TextField()
    valor_novo = models.TextField()
    data = models.DateTimeField(auto_now_add=True)