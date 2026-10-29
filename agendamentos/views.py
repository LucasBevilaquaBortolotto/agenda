from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail

from django.db import transaction
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from agendamentos.forms import AgendamentoListForm, AgendamentoModelForm, AgendamentosServicoInline
from agendamentos.models import Agendamento


class AgendamentosView(LoginRequiredMixin,ListView):
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

class AgendamentoAddView(LoginRequiredMixin, AgendamentoFormsetMixin, CreateView):
    model = Agendamento
    form_class = AgendamentoModelForm
    template_name = 'agendamento_form.html'
    success_url = reverse_lazy('agendamentos')
    success_message = 'Agendamento criado com sucesso!'


class AgendamentoUpdateView(LoginRequiredMixin,AgendamentoFormsetMixin, UpdateView):
    model = Agendamento
    form_class = AgendamentoModelForm
    template_name = 'agendamento_form.html'
    success_url = reverse_lazy('agendamentos')
    success_message = 'Agendamento atualizado com sucesso!'

class AgendamentoDeleteView(LoginRequiredMixin,SuccessMessageMixin, DeleteView):
    model = Agendamento
    template_name = 'agendamento_apagar.html'
    success_url = reverse_lazy('agendamentos')
    success_message = 'Agendamento apagado com sucesso!'



class AgendamentoExibir(LoginRequiredMixin,DetailView):
    model = Agendamento
    template_name = 'agendamento_exibir.html'
    def post(self, request, *args, **kwargs):
        agendamento = self.get_object()
        sucesso, mensagem = agendamento.finalizar_atendimento()
        if sucesso:
            messages.success(request, mensagem)
            self.enviar_email(agendamento)
        else:
            messages.warning(request, mensagem)
        return redirect('agendamento_exibir', pk=agendamento.pk)

    def enviar_email(self, agendamento):
        email = []
        email.append(agendamento.cliente.email)
        descricao = []
        for servico in agendamento.ordem_servicos_agendamento.all():
            descricao.append(f'{servico} - R$ {servico.preco} ({servico.get_situacao_display()})')

        dados = {'cliente': agendamento.cliente.nome,
                 'horario': agendamento.horario,
                 'funcionario': agendamento.funcionario.nome,
                 'descricao': descricao,
                 'valor': agendamento.valor,}

        texto_email = render_to_string('emails/texto_email.txt', dados)
        html_email = render_to_string('emails/texto_email.html', dados)
        send_mail(subject='Lavacar - Serviço concluido',
                  message=texto_email,
                  from_email='cassal@politecnico.ufsm.br',
                  recipient_list=email,
                  html_message=html_email,
                  fail_silently=False,
                  )
        return redirect('agendamentos')
