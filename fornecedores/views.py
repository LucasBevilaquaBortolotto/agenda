from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import FornecedorModelForm
from .models import Fornecedor


class FornecedoresView(ListView):
    model = Fornecedor
    template_name = 'fornecedores.html'
    context_object_name = 'fornecedores'
    paginate_by = 20

    def get_queryset(self):
        buscar = self.request.GET.get('buscar')
        qs = super().get_queryset()
        if buscar:
            qs = qs.filter(nome__icontains=buscar)
        return qs


class FornecedorAddView(SuccessMessageMixin,CreateView):
    model = Fornecedor
    form_class = FornecedorModelForm
    template_name = 'fornecedor_form.html'
    success_url = reverse_lazy('fornecedores')
    success_message = 'Fornecedor cadstrado com sucesso!'

class FornecedorUpdateView(SuccessMessageMixin,UpdateView):
    model = Fornecedor
    form_class = FornecedorModelForm
    template_name = 'fornecedor_form.html'
    success_url = reverse_lazy('fornecedores')
    success_message = 'Fornecedor atualizado com sucesso!'

class FornecedorDeleteView(SuccessMessageMixin,DeleteView):
    model = Fornecedor
    template_name = 'fornecedor_apagar.html'
    success_url = reverse_lazy('fornecedores')
    success_message = 'Fornecedor apagado com sucesso!'

    def post(self,request,*args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            return super().post(request,*args,**kwargs)
        except ProtectedError:
            messages.error(request, f'O fornecedor {self.object} não pode ser excluido'
                           f'Esse fornecedor esta regitrado no fornecimento de produtos')

            return redirect(success_url)
# Create your views here.
