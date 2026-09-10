from django.db import models

class Fornecedor(models.Model):
    nome = models.CharField('Nome', max_length=70, help_text='Nome do fornecedor')
    cnpj = models.CharField('Cnpj', max_length=20, help_text='Cnpj do fornecedor', unique=True)
    fone = models.CharField('Fone', max_length=20, help_text='Fone')

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'


    def __str__(self):
        return self.nome
