from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from funcionarios.forms import FuncionarioModelForm
from funcionarios.models import Funcionario


class FuncionariosView(ListView):
    model = Funcionario
    template_name = 'funcionarios.html'
    context_object_name = 'funcionarios'
    paginate_by = 20

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super().get_queryset()
        if buscar:
            qs = qs.filter(nome__icontains=buscar)
        return qs


class FuncionarioAddView(SuccessMessageMixin, CreateView):
    model = Funcionario
    form_class = FuncionarioModelForm
    template_name = 'funcionario_form.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionario criado com sucesso'

class FuncioanrioUpdateView(SuccessMessageMixin, UpdateView):
    model = Funcionario
    form_class = FuncionarioModelForm
    template_name = 'funcionario_form.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionario atualizado com sucesso'

class FuncionarioDeleteView(SuccessMessageMixin, DeleteView):
    model = Funcionario
    template_name = 'funcionario_apagar.html'
    success_url = reverse_lazy('funcionarios')
    success_message = 'Funcionario apagado com sucesso'


    def post(self,request,*args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            return super().post(request,*args,**kwargs)
        except ProtectedError:
            messages.error(request, f'O funcionario {self.object} não pode ser excluido'
                           f'Esse funcionario esta regitrado no fornecimento de produtos')

            return redirect(success_url)