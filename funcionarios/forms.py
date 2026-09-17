from django import forms

from .models import Funcionario


class FuncionarioModelForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'funcao', 'fone', 'email','data_admissao','foto']

        error_messages = {
            'nome': {'required': 'O nome do funcionario é um campo Obriatorio'},
            'funcao': {'required': 'A função é obrigatoria'},
            'fone': {'required': 'O numero de telefone é um campo Obriatorio'},
            'email': {'required': 'O e-mail do funcionario é um campo Obriatorio','invalid': 'Formato invalido. Exemplo: fulano@dominio.com','unique':'E-mail ja cadastrado'},
            'data_admissao': {'required': 'A data de admissao Obrigatoria'},
        }