from django.urls import path
from agenda.views import AgendamentoDetail, AgendamentoList, get_gera_relatorio_prestadores, get_horario, healthcheck

urlpatterns = [
   path('agendamentos/', AgendamentoList.as_view()),
   path('agendamentos/<int:pk>/', AgendamentoDetail.as_view()),
   path('prestadores/', get_gera_relatorio_prestadores, name='get_gera_relatorio_prestadores'),
   path('horarios/', get_horario, name='get_horario'),
   path('', healthcheck)
]