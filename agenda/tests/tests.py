from datetime import datetime, timezone
import json
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from unittest import mock

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
      
      
   def test_listagem_filtra_cancelados(self):
      user = User.objects.create_user(username="prestador", password="senha")
      self.client.force_authenticate(user=user)
      # Cria um agendamento cancelado e um não cancelado
      Agendamento.objects.create(
         data_horario=datetime(2026, 8, 2, 9, 0, tzinfo=timezone.utc),
         nome_cliente="Cliente 1",
         email_cliente="cliente1@email.com",
         telefone_cliente="92988339327",
         cancelado=True,
         prestador=user,
      )
      Agendamento.objects.create(
         data_horario=datetime(2026, 8, 2, 10, 0, tzinfo=timezone.utc),
         nome_cliente="Cliente 2",
         email_cliente="cliente2@email.com",
         telefone_cliente="92988339327",
         cancelado=False,
         prestador=user,
      )
      # Filtra cancelados
      response = self.client.get("/api/agendamentos/?username=prestador&cancelado=true")
      data = json.loads(response.content)
      self.assertEqual(len(data), 1)
      self.assertTrue(data[0]["cancelado"])
      # Filtra não cancelados
      response = self.client.get("/api/agendamentos/?username=prestador&cancelado=false")
      data = json.loads(response.content)
      self.assertEqual(len(data), 1)
      self.assertFalse(data[0]["cancelado"])
      
      
class TestCriacaoAgendamento(APITestCase):
   def test_cria_agendamento(self):
      user = User.objects.create_user(username="prestador", password="senha")
      
      agendamento_request_data = {
         "data_horario": "2026-08-02T09:00:00Z", 
         "nome_cliente": "Thiago",
         "email_cliente": "tcardosonobre@gmail.com",
         "telefone_cliente": "92988339327",
         "cancelado": False,
         "prestador": "prestador"
      }
      
      self.client.force_authenticate(user=user)
      response = self.client.post("/api/agendamentos/", agendamento_request_data, format="json")
      print(response.data)
      self.assertEqual(response.status_code, 201)
      
      response_get = self.client.get("/api/agendamentos/?username=prestador")
      self.assertEqual(response_get.status_code, 200)
      
      data = json.loads(response_get.content)
      
      agendamento_serialiazado = {
         "id": 1,
         "data_horario": "2026-08-02T09:00:00Z",
         "nome_cliente": "Thiago",
         "email_cliente": "tcardosonobre@gmail.com",
         "telefone_cliente": "92988339327",
         "cancelado": False,
         "prestador": "prestador"
      }
      
      self.assertEqual(data[0], agendamento_serialiazado)
      
   
   def test_cria_agendamento_no_passado_retorna_400(self):
      user = User.objects.create_user(username="prestador", password="senha")
      
      agendamento_request_data = {
         "data_horario": "2020-08-02T09:00:00Z", 
         "nome_cliente": "Thiago",
         "email_cliente": "tcardosonobre@gmail.com",
         "telefone_cliente": "92988339327",
         "cancelado": False,
         "prestador": "prestador"
      }
      
      self.client.force_authenticate(user=user)
      response = self.client.post("/api/agendamentos/", agendamento_request_data, format="json")
      print(response.data)
      self.assertEqual(response.status_code, 400)
      
     
      
      
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
      
   
class TestGetHorarios(APITestCase):
   @mock.patch("agenda.libs.brasil_api.is_feriado", return_value=True)
   def test_quando_data_e_feriado_retorna_lista_vazia(self, _):
      user = User.objects.create_user(username="prestador", password="senha")
      self.client.force_authenticate(user=user)
      response = self.client.get("/api/horarios/?data=2025-12-25")
      data = json.loads(response.content)
      self.assertEqual(data, [])
      
   @mock.patch("agenda.libs.brasil_api.is_feriado", return_value=False)
   def test_quando_data_nao_e_feriado_retorna_horarios_disponiveis(self, _):
      user = User.objects.create_user(username="prestador", password="senha")
      self.client.force_authenticate(user=user)
      response = self.client.get("/api/horarios/?data=2026-08-02")
      data = json.loads(response.content)
      
      self.assertNotEqual(data, [])
      self.assertEqual(data[0], "2026-08-02T09:00:00Z")
      self.assertEqual(data[-1], "2026-08-02T17:30:00Z")