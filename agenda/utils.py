from typing import Iterable
from datetime import date, datetime, timezone, timedelta
import requests

from agenda.libs import brasil_api
from agenda.models import Agendamento

def get_horarios_disponiveis(data: datetime.date) -> Iterable[datetime]:
   """
   Retorna uma lista com objetos do tipo datetime cujas datas são o mesmo dia passado (data)
   e os horários são os horários disponíveis para aquele dia, conforme outros agendamentos existam.
   """
   if brasil_api.is_feriado(data):
      return []
   
   start = datetime(year=data.year, month=data.month, day=data.day, hour=9, minute=0, tzinfo=timezone.utc)
   end = datetime(year=data.year, month=data.month, day=data.day, hour=18, minute=0, tzinfo=timezone.utc)
   delta = timedelta(minutes=30)
   horarios_disponiveis = set()
   while start < end:
      if not Agendamento.objects.filter(data_horario=start, cancelado=False).exists():
         horarios_disponiveis.add(start)
      start = start + delta
      
   return horarios_disponiveis