from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.db.models.functions import Upper


class Servico(models.Model):
    nome = models.CharField('Nome',max_length=100, help_text='Nome do servico', unique=True)
    preco = models.DecimalField('Preço', max_digits=5, decimal_places=2, help_text='Preço do serviço',validators=[MinValueValidator(Decimal('0.01'))])
    descricao = models.TextField('Descrição', max_length=300, help_text='Descrição e observações do serviço')
    produtos = models.ManyToManyField('produtos.Produto', through='servicos.ProdutosServico', related_name='servico_produtos')

    class Meta:
        verbose_name = 'Servico'
        verbose_name_plural = 'Servicos'
        ordering = [Upper ('nome')]

    def __str__(self):
        return self.nome





class ProdutosServico(models.Model):
    servico = models.ForeignKey('servicos.Servico',verbose_name='Serviço', on_delete=models.CASCADE,related_name='produtos_servico_servico')
    produto = models.ForeignKey('produtos.Produto',verbose_name='Produto', on_delete=models.PROTECT,related_name='produtos_servico_produto')
    quantidade = models.DecimalField('Quantidade', max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

    class Meta:
        verbose_name = 'Produto utilizado'
        verbose_name_plural = 'Produtos utilizados'

        constraints = [models.UniqueConstraint(fields=['servico','produto'], name='constraint_produto_servico'),
                      models.CheckConstraint(condition=Q(quantidade__gte=Decimal('0.01')),name='quantidade_produto_servico_maior_que_zero')
                      ]
    def __str__(self):
        return f'{self.produto}'