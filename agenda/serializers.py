from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from agenda.libs import brasil_api
from agenda.models import Agendamento
from agenda import utils


class AgendamentoSerializer(serializers.ModelSerializer):
   class Meta:
      model = Agendamento
      fields = ["id", "prestador", "data_horario", "nome_cliente", "email_cliente", "telefone_cliente", "cancelado"]
   
   prestador = serializers.CharField()
   
   def validate_prestador(self, value):
      try:
         prestador_obj = User.objects.get(username=value)
      except User.DoesNotExist:
         raise serializers.ValidationError("Username não existe!")
      return prestador_obj
   
   
   def validate_data_horario(self, value):
      if value < timezone.now():
         raise serializers.ValidationError("Agendamento não pode ser feito no passado!")
      # Validação de feriado
      if brasil_api.is_feriado(value.date()):
         raise serializers.ValidationError("Não é possível agendar em feriados!")
      if not value in utils.get_horarios_disponiveis(value.date()):
         raise serializers.ValidationError("Horário não disponível para agendamento!")
      return value
   
   
   def validate(self, attrs):
      telefone_cliente = attrs.get("telefone_cliente", "")
      email_cliente = attrs.get("email_cliente", "")
      
      if email_cliente.endswith(".br") and telefone_cliente.startswith("+") and not telefone_cliente.startswith("+55"):
         raise serializers.ValidationError("Email brasileiro deve estar associado a telefone do Brasil (+55)")
      return attrs
   
   
class PrestadorSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ["id", "username", "agendamentos"]
      
   agendamentos = AgendamentoSerializer(many=True, read_only=True) 