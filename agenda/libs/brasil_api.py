import requests
from datetime import date
from django.conf import TESTING

def is_feriado(data: date) -> bool:
   if TESTING == True:
      if date.day == 25 and date.month == 12:
         return True
      return False
   
   ano = data.year
   r = requests.get(f"https://brasilapi.com.br/api/feriados/v1/{ano}")
   if r.status_code != 200:
      raise ValueError("Erro ao buscar feriados!")
   
   feriados = r.json()
   for feriado in feriados:
      data_feriado_as_str = feriado["date"]
      data_feriado = date.fromisoformat(data_feriado_as_str)
      if data == data_feriado:
         return True
      
   return False