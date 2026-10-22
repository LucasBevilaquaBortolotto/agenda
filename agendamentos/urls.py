from django.urls import path

from .views import AgendamentosView, AgendamentoAddView, AgendamentoUpdateView, AgendamentoDeleteView, AgendamentoExibir

urlpatterns = [
    path('agendamentos', AgendamentosView.as_view(), name='agendamentos'),
    path('agendamentos/novo/', AgendamentoAddView.as_view(), name='agendamentos_adicionar'),
    path('agendamentos/<int:pk>/editar/', AgendamentoUpdateView.as_view(), name='agendamentos_editar'),
    path('agendamentos/<int:pk>/apagar/', AgendamentoDeleteView.as_view(), name='agendamentos_apagar'),
    path('agendamentos/<int:pk>/exibir/', AgendamentoExibir.as_view(), name='agendamento_exibir'),
]