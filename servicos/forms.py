from django import forms

from .models import Servico

class ServicoModelForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'descricao', 'preco']

        error_messages = {
            'nome': {'required': 'O nome do serviço é Obrigatorio', 'unique': 'Serviço ja cadastrado'},
            'descricao': {'required': 'A descrição do serviço é obrigatoria'},
            'preco': {'required': 'O preço é Obrigatorio'},
        }