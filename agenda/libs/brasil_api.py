import requests
from datetime import date
from django.conf import settings
import logging


def is_feriado(date: date):
   logging.info(f"Fazendo requisição para BrasilAPI para a data: {date.isoformat()}")
   if settings.TESTING:
      logging.info("Requisição não está sendo feita, pois TESTING = True")
      if date.day == 25 and date.month == 12:
         return True
      return False
   
   ano = date.year
   r = requests.get(f"https://brasilapi.com.br/api/feriados/v1/{ano}")
   if r.status_code != 200:
      logging.error(f"Algum erro ocorreu na BrasilAPI")
      #raise ValueError("Erro ao buscar feriados!")
   
   feriados = r.json()
   for feriado in feriados:
      data_feriado_as_str = feriado["date"]
      data_feriado = date.fromisoformat(data_feriado_as_str)
      if date == data_feriado:
         return True
      
   return False