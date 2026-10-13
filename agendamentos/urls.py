from django.urls import path

from .views import AgendamentosView,AgendamentoAddView,AgendamentoUpdateView,AgendamentoDeleteView

urlpatterns = [
    path('agendamentos', AgendamentosView.as_view(), name='agendamentos'),
    path('agendamentos/novo/', AgendamentoAddView.as_view(), name='agendamentos_adicionar'),
    path('agendamentos/<int:pk>/editar/', AgendamentoUpdateView.as_view(), name='agendamentos_editar'),
    path('agendamentos/<int:pk>/apagar/', AgendamentoDeleteView.as_view(), name='agendamentos_apagar'),
]