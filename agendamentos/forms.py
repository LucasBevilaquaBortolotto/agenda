from django import forms
from django.forms import inlineformset_factory

from agendamentos.models import Agendamento, OrdemServicos
from clientes.models import Cliente
from funcionarios.models import Funcionario
from servicos.models import ProdutosServico


class AgendamentoListForm(forms.Form):
    cliente = forms.ModelChoiceField(label="Cliente", queryset=Cliente.objects.all(), required=False)
    funcionario = forms.ModelChoiceField(label='Funcionario', queryset=Funcionario.objects.all(), required=False)


class AgendamentoModelForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['horario','cliente', 'funcionario']


        error_messages = {
            'horario': {'required':'Horario Obrigatorio'},
            'cliente': {'required': 'Cliente Obrigatorio'},
            'funcionario': {'required': 'Funcionario Obrigatorio'}
        }
class BaseOrdemServicoFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        for form in self.forms:
            if not form.cleaned_data or form.cleaned_data.get('DELETE'):
                continue
            situacao = form.cleaned_data.get('situacao')
            servico = form.cleaned_data.get('servico')
            if situacao == 'R' and servico:
                insumos = ProdutosServico.objects.filter(servico=servico).select_related('produto')
                itens_sem_estoque = []
                for insumo in insumos:
                    produto = insumo.produto
                    if produto.quantidade < insumo.quantidade:
                        itens_sem_estoque.append(
                            f"{produto.nome}(Estoque atual: {produto.quantidade} | Exigido: {insumo.quantidade})"
                        )
                if itens_sem_estoque:
                    lista_produtos = ", ".join(itens_sem_estoque)
                    form.add_error(
                    None,
                    f"Estoque insuficiente para: {lista_produtos}"
                    )

AgendamentosServicoInline = inlineformset_factory(Agendamento, OrdemServicos,fields=('servico','funcionario','situacao','observacoes'),extra=1, can_delete=True, formset=BaseOrdemServicoFormSet)

