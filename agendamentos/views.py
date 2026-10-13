from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from agendamentos.forms import AgendamentoListForm, AgendamentoModelForm
from agendamentos.models import Agendamento


class AgendamentosView(ListView):
    model = Agendamento
    template_name = 'agendamentos.html'
    context_object_name = 'agendamentos'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        self.filter_form = AgendamentoListForm(self.request.GET or None)

        if self.filter_form.is_valid():
            cliente = self.filter_form.cleaned_data.get('cliente')
            funcionario = self.filter_form.cleaned_data.get('funcionario')

            if cliente:
                qs = qs.filter(cliente=cliente)
            if funcionario:
                qs = qs.filter(funcionario=funcionario)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.filter_form

        params = self.request.GET.copy()
        params.pop('page', None)
        context['query_params'] = params.urlencode()
        return context


class AgendamentoAddView(SuccessMessageMixin, CreateView):
    model = Agendamento
    form_class = AgendamentoModelForm
    template_name = 'agendamento_form.html'
    success_url = reverse_lazy('agendamentos')
    success_message = 'Agendamento criado com sucesso!'


class AgendamentoUpdateView(SuccessMessageMixin, UpdateView):
    model = Agendamento
    form_class = AgendamentoModelForm
    template_name = 'agendamento_form.html'
    success_url = reverse_lazy('agendamentos')
    success_message = 'Agendamento atualizado com sucesso!'

class AgendamentoDeleteView(SuccessMessageMixin, DeleteView):
    model = Agendamento
    template_name = 'agendamento_apagar.html'
    success_url = reverse_lazy('agendamentos')
    success_message = 'Agendamento apagado com sucesso!'