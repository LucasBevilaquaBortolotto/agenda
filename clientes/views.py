from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from clientes.forms import ClienteModelForm
from clientes.models import Cliente


class ClientesView(PermissionRequiredMixin,ListView):
    permission_required = 'clientes.view_cliente'
    permission_denied_message = 'Visualizar cliente'
    model = Cliente
    template_name = 'clientes.html'
    context_object_name = 'clientes'
    paginate_by = 20

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super().get_queryset()
        if buscar:
            qs = qs.filter(nome__icontains=buscar)
        return qs


class ClienteAddView(PermissionRequiredMixin,SuccessMessageMixin, CreateView):
    permission_required = 'clientes.add_cliente'
    permission_denied_message = 'Cadastrar Cliente'
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente Cadastrado'

class ClienteUpdateView(PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = 'clientes.change_cliente'
    permission_denied_message = 'Editar Cliente'
    model = Cliente
    form_class = ClienteModelForm
    template_name = 'cliente_form.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente Alterado com sucesso'

class ClienteDeleteView(PermissionRequiredMixin,SuccessMessageMixin, DeleteView):
    permission_required = 'clientes.delete_cliente'
    permission_denied_message = 'Deletar Cliente'
    model = Cliente
    template_name = 'cliente_apagar.html'
    success_url = reverse_lazy('clientes')
    success_message = 'Cliente apagado com sucesso'


    def post(self,request,*args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            return super().post(request,*args,**kwargs)
        except ProtectedError:
            messages.error(request, f'O Cliente {self.object} não pode ser excluido'
                           f'Esse cliente esta regitrado no fornecimento de produtos')

            return redirect(success_url)

