from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Q, ProtectedError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from servicos.forms import ServicoModelForm, ProdutosServicoInLine
from servicos.models import Servico


class ServicosView(ListView):
    model = Servico
    template_name = 'servicos.html'
    context_object_name = 'servicos'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related('produtos_servico_servico__produto')

        buscar = self.request.GET.get('buscar')
        if buscar:
            qs = qs.filter(Q(nome__icontains=buscar) | Q(descricao__icontains=buscar))
        return qs


class ServicoFormsetMixin:
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if 'frm_inline' not in data:
           from produtos.models import Produto
           produtos_qs = Produto.objects.all()
           if self.request.POST:
               formset = ProdutosServicoInLine(self.request.POST, instance=self.object)
           else:
               formset = ProdutosServicoInLine(instance=self.object)
           for form in formset.forms:
               form.fields['produto'].queryset = produtos_qs
           data['frm_inline'] = formset
        return data

    def form_valid(self,form):
        from produtos.models import Produto
        produtos_qs = Produto.objects.all()
        frm_inline = ProdutosServicoInLine(self.request.POST, instance=self.object)
        for f in frm_inline.forms:
            f.fields['produto'].queryset = produtos_qs
        if form.is_valid() and frm_inline.is_valid():
            with transaction.atomic():
                self.object = form.save()
                frm_inline.instance = self.object
                frm_inline.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form, frm_inline)

    def form_invalid(self, form, frm_inline=None):
        if frm_inline is None:
            frm_inline = ProdutosServicoInLine(self.request.POST, instance=self.object)
        return self.render_to_response(
            self.get_context_data(form=form, frm_inline=frm_inline)
        )



class ServicoAddView(SuccessMessageMixin, ServicoFormsetMixin ,CreateView, ):
    model = Servico
    form_class = ServicoModelForm
    template_name = 'servico_form.html'
    success_url = reverse_lazy('servicos')
    success_message = 'Servico adicionado com sucesso'

class ServicoUpdateView(SuccessMessageMixin,ServicoFormsetMixin, UpdateView):
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


    def post(self,request,*args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            return super().post(request,*args,**kwargs)
        except ProtectedError:
            messages.error(request, f'O Serviço {self.object} não pode ser excluido'
                           f'Esse Serviço esta regitrado no fornecimento de produtos')

            return redirect(success_url)

