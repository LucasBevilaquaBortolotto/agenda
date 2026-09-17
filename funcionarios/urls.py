from django.urls import path

from .views import FuncionariosView, FuncionarioAddView, FuncioanrioUpdateView, FuncionarioDeleteView

urlpatterns = [
    path('funcionarios', FuncionariosView.as_view(), name='funcionarios'),
    path('funcionarios/novo/', FuncionarioAddView.as_view(), name='funcionario_adicionar'),
    path('funcionarios/<int:pk>/editar/', FuncioanrioUpdateView.as_view(), name='funcionario_editar'),
    path('funcionarios/<int:pk>/apagar/', FuncionarioDeleteView.as_view(), name='funcionario_apagar'),
]