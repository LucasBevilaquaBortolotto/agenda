from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.db.models import Q, Sum

from servicos.models import ProdutosServico


class Agendamento(models.Model):
    horario = models.DateTimeField('Horario', help_text='Data e hora do atendimento')
    cliente = models.ForeignKey('clientes.CLiente', verbose_name='Cliente', help_text='Nome do cliente', on_delete=models.PROTECT)
    funcionario = models.ForeignKey('funcionarios.Funcionario',verbose_name='Funcionario', help_text='Nome do funcionario',  on_delete=models.PROTECT)
    servicos = models.ManyToManyField('servicos.Servico', verbose_name='Serviço', through='agendamentos.OrdemServicos')
    valor = models.DecimalField('Valor total', max_digits=6, decimal_places=2, default=0.00)
    status = models.CharField('Status', max_length=1, help_text='Status do agendamento', default='A')

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['-horario']

    def atualizar_valor_total(self):
        total = self.ordem_servicos_agendamento.filter(~Q(situacao='C')).aggregate(total=Sum('preco'))['total'] or Decimal('0.00')
        Agendamento.objects.filter(pk=self.pk).update(valor=total)
        self.valor = total

    def finalizar_atendimento(self):
        if self.status != 'A':
            return False, "Este agendamento ja esta finalizado ou cancelado"
        if self.ordem_servicos_agendamento.filter(situacao='A').exists():
            return False, "Existem Serviços com a situação em aberto"
        with transaction.atomic():
            for ordem in self.ordem_servicos_agendamento.filter(situacao='R'):
                insumos = ProdutosServico.objects.filter(servico=ordem.servico).select_related('produto')
                for insumo in insumos:
                    produto = insumo.produto
                    produto.quantidade -= insumo.quantidade
                    produto.save()
            self.status = 'F'
            self.save()
        return True, "Agendamento finalizado com sucesso"

    def __str__(self):
        return f'Cliente: {self.cliente}'


class OrdemServicos(models.Model):
    SITUACAO_OPCOES = (
    ('A','Agendado'),
    ('B','Realizado'),
    ('C','Cancelado'),
    )
    agendamento = models.ForeignKey('agendamentos.Agendamento', verbose_name='Agendamento', on_delete=models.CASCADE,related_name='ordem_servicos_agendamento')
    servico = models.ForeignKey('servicos.Servico', verbose_name='Serviço', on_delete=models.PROTECT,related_name='ordem_servicos_servico')
    funcionario = models.ForeignKey('funcionarios.Funcionario', verbose_name='Funcionario', on_delete=models.PROTECT,related_name='ordem_servicos_funcionario')
    situacao = models.CharField('Situação', max_length=1, choices=SITUACAO_OPCOES, default='A')
    observacoes = models.TextField('Observações', max_length=300, blank=True, null=True)
    preco = models.DecimalField('Preço', max_digits=6, decimal_places=2, help_text='Preço do serviço', validators=[MinValueValidator(Decimal('0.01'))])

    class Meta:
        verbose_name = 'Serviço realizado'
        verbose_name_plural = 'Serviços realizados'

        constraints = [models.UniqueConstraint(fields=['agendamento','servico'], name='constraint_agendamento')]


    def save(self, *args, **kwargs):
        if not self.pk and not self.preco:
            self.preco = self.servico.preco
        super().save(*args, **kwargs)
        self.agendamento.atualizar_valor_total()

    def delete(self, *args, **kwargs):
        agendamento = self.agendamento
        super().delete(*args, **kwargs)
        agendamento.atualizar_valor_total()

    def __str__(self):
        return self.servico.nome


