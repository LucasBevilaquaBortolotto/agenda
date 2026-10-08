from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from servicos.forms import ServicoModelForm
from servicos.models import Servico


class ServicosView(ListView):
    model = Servico
    template_name = 'servicos.html'
    context_object_name = 'servicos'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()

        buscar = self.request.GET.get('buscar')
        if buscar:
            qs = qs.filter(Q(nome__icontains=buscar) | Q(descricao__icontains=buscar))
        return qs



class ServicoAddView(SuccessMessageMixin, CreateView):
    model = Servico
    form_class = ServicoModelForm
    template_name = 'servico_form.html'
    success_url = reverse_lazy('servicos')
    success_message = 'Servico adicionado com sucesso'

class ServicoUpdateView(SuccessMessageMixin, UpdateView):
    model = Servico
    form_class = ServicoModelForm
    template_name = 'servico_form.html'
    success_url = reverse_lazy('servicos')
    success_message = 'Servico atualizado com sucesso'

class ServicoDeleteView(SuccessMessageMixin, DeleteView):
    model = Servico
    template_name = 'servico_apagar.html'
    success_url = reverse_lazy('servicos')
    success_message = 'Servico apagado com sucesso'
