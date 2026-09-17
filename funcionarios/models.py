from django.db import models

from clientes.models import Pessoa

class Funcionario(Pessoa):
    funcao = models.CharField('Função', max_length=100,help_text='Função na Empresa')
    data_admissao = models.DateField('Admissão', help_text='Data de admissão')

    class Meta:
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'


    def __str__(self):
        return self.nome
