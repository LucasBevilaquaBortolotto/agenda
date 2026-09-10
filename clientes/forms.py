from django import forms

from .models import Cliente


class ClienteModelForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'endereco', 'fone','email','foto']

        error_messages = {
            'nome': {'required': 'O nome campo obrigatorio'},
            'endereco': {'required': 'O endereco campo obrigatorio'},
            'fone': {'required': 'O fone campo obrigatorio'},
            'email': {'required': 'O email campo obrigatorio',
                      'invalid': 'Formato invalido',
                      'unique': 'email ja cadastrado'
                      },
        }