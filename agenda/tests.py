from datetime import datetime, timezone
import json
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from agenda.models import Agendamento

# Create your tests here.
class TestListagemAgendamentos(APITestCase):
   def test_listagem_vazia(self):
      user = User.objects.create_user(username="prestador", password="senha")
      self.client.force_authenticate(user=user)
      response = self.client.get("/api/agendamentos/?username=prestador")
      data = json.loads(response.content)
      self.assertEqual(data, [])
      
      
   def test_listagem_de_agendamentos_criados(self):  
      user = User.objects.create_user(username="prestador", password="senha")    
      Agendamento.objects.create(
         data_horario = datetime(2025, 8, 2, tzinfo=timezone.utc),
         nome_cliente = "Thiago",
         email_cliente = "tcardosonobre@gmail.com",
         telefone_cliente = "92988339327",
         cancelado = False,
         prestador = user,
      )
      
      agendamento_serialiazado = {
         "id": 1,
         "data_horario": "2025-08-02T00:00:00Z",
         "nome_cliente": "Thiago",
         "email_cliente": "tcardosonobre@gmail.com",
         "telefone_cliente": "92988339327",
         "cancelado": False,
         "prestador": "prestador"
      }
      
      self.client.force_authenticate(user=user)
      response = self.client.get("/api/agendamentos/?username=prestador")
      data = json.loads(response.content)
      self.assertDictEqual(data[0], agendamento_serialiazado)
      
      
class TestCriacaoAgendamento(APITestCase):
   def test_cria_agendamento(self):
      user = User.objects.create_user(username="prestador", password="senha")
      
      agendamento_request_data = {
         "data_horario": "2026-08-02T00:00:00Z", 
         "nome_cliente": "Thiago",
         "email_cliente": "tcardosonobre@gmail.com",
         "telefone_cliente": "92988339327",
         "cancelado": False,
         "prestador": "prestador"
      }
      
      self.client.force_authenticate(user=user)
      response = self.client.post("/api/agendamentos/", agendamento_request_data, format="json")
      self.assertEqual(response.status_code, 201)
      
      response_get = self.client.get("/api/agendamentos/?username=prestador")
      self.assertEqual(response_get.status_code, 200)
      
      data = json.loads(response_get.content)
      
      agendamento_serialiazado = {
         "id": 1,
         "data_horario": "2026-08-02T00:00:00Z",
         "nome_cliente": "Thiago",
         "email_cliente": "tcardosonobre@gmail.com",
         "telefone_cliente": "92988339327",
         "cancelado": False,
         "prestador": "prestador"
      }
      
      self.assertEqual(data[0], agendamento_serialiazado)
      
      
   def test_quando_o_request_e_invalido_retorna_400(self):
      User.objects.create_user(username="prestador", password="senha")
      
      agendamento_request_data = {
         "data_horario": "-08-02T00:00:00Z", # Data inválida
         "nome_cliente": "Thiago",
         "email_cliente": "tcardosonobre@gmail.com",
         "telefone_cliente": "92988339327",
         "cancelado": False,
         "prestador": "prestador"
      }
      
      response = self.client.post("/api/agendamentos/", agendamento_request_data, format="json")
      self.assertEqual(response.status_code, 400)
      
   
   def test_cria_agendamento_em_feriado_retorna_400(self):
      User.objects.create_user(username="prestador", password="senha")
      agendamento_request_data = {
         "data_horario": "2026-12-25T10:00:00Z",  # Natal, feriado
         "nome_cliente": "Thiago",
         "email_cliente": "tcardosonobre@gmail.com",
         "telefone_cliente": "92988339327",
         "cancelado": False,
         "prestador": "prestador"
      }
      response = self.client.post("/api/agendamentos/", agendamento_request_data, format="json")
      self.assertEqual(response.status_code, 400)
      self.assertIn("Não é possível agendar em feriados!", str(response.data))
      