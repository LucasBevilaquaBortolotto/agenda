from django import forms
from .models import Fornecedor

class FornecedorModelForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = '__all__'

        error_messages = {
            'nome': {'required': 'O nome do fornecedor é um campo obrigatório'},
            'cnpj': {'required': 'O cnpj é um campo obrigatorio', 'unique': 'Cnpj ja cadastrado'},
            'fone': {'required': 'O numero de telefone é obriatorio'}
        }