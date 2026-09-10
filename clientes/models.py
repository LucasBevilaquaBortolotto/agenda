from django.db import models

class Pessoa(models.Model):
    nome = models.CharField('Nome', max_length=50, help_text='Nome Completo')
    fone = models.CharField('Fone', max_length=15, help_text='Numero do Telefone')
    email = models.EmailField('E-mail', max_length=100, help_text='Endereço de email', unique=True)
    foto = models.ImageField('Foto', upload_to='fotos', null=True, blank=True)


    class Meta:
        abstract = True

        def __str__(self):
            return self.nome


class Cliente(Pessoa):
    endereco = models.CharField('Endereço', max_length=100, help_text='Endereço Completo')


    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

        def __str__(self):
            return super().nome
# Create your models here.
