from django.urls import path

from .views import ServicosView,ServicoAddView,ServicoUpdateView,ServicoDeleteView

urlpatterns = [
    path('servicos', ServicosView.as_view(), name='servicos'),
    path('servicos/novo/', ServicoAddView.as_view(), name='servico_adicionar'),
    path('servicos/<int:pk>/editar/', ServicoUpdateView.as_view(), name='servico_editar'),
    path('servicos<int:pk>/apagar/', ServicoDeleteView.as_view(), name='servico_apagar'),
]