from django.urls import path

from .views import FornecedoresView, FornecedorAddView, FornecedorUpdateView, FornecedorDeleteView


urlpatterns = [
    path('fornecedores', FornecedoresView.as_view(), name='fornecedores'),
    path('fornecedores/novo/',FornecedorAddView.as_view(),name='fornecedor_adicionar'),
    path('fornecedores/<int:pk>/editar/',FornecedorUpdateView.as_view(),name='fornecedor_editar'),
    path('fornecedores/<int:pk>/apagar',FornecedorDeleteView.as_view(),name='fornecedor_apagar'),
]