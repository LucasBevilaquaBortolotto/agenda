from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

class Servico(models.Model):
    nome = models.CharField('Nome',max_length=100, help_text='Nome do servico', unique=True)
    preco = models.DecimalField('Preço', max_digits=5, decimal_places=2, help_text='Preço do serviço',validators=[MinValueValidator(Decimal('0.01'))])
    descricao = models.TextField('Descrição', max_length=300, help_text='Descrição e observações do serviço')

class Meta:
    verbose_name = 'Servico'
    verbose_name_plural = 'Servicos'

def __str__(self):
    return self.nome