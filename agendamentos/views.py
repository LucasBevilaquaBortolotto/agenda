from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from agendamentos.forms import AgendamentoListForm, AgendamentoModelForm, AgendamentosServicoInline
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


class AgendamentoFormsetMixin:
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['frm_inline'] = AgendamentosServicoInline(self.request.POST, instance=self.object)
        else:
            data['frm_inline'] = AgendamentosServicoInline(instance=self.object)

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        frm_inline = context['frm_inline']

        if frm_inline.is_valid():
            with transaction.atomic():
                self.object = form.save()
                frm_inline.instance = self.object
                frm_inline.save()
            if hasattr(self,'success_message'):
                messages.success(self.request, self.success_message)
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class AgendamentoAddView(AgendamentoFormsetMixin, CreateView):
    model = Agendamento
    form_class = AgendamentoModelForm
    template_name = 'agendamento_form.html'
    success_url = reverse_lazy('agendamentos')
    success_message = 'Agendamento criado com sucesso!'


class AgendamentoUpdateView(AgendamentoFormsetMixin, UpdateView):
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



class AgendamentoExibir(DetailView):
    model = Agendamento
    template_name = 'agendamento_exibir.html'
    def post(self, request, *args, **kwargs):
        agendamento = self.get_object()
        sucesso, mensagem = agendamento.finalizar_atendimento()
        if sucesso:
            messages.success(request, mensagem)
        else:
            messages.warning(request, mensagem)
        return redirect('agendamento_exibir', pk=agendamento.pk)

