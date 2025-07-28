from rest_framework import serializers

from agenda.models import Agendamento


class AgendamentoSerializer(serializers.Serializer):
   data_horario = serializers.DateTimeField()
   nome_cliente = serializers.CharField(max_length=200)
   email_cliente = serializers.EmailField()
   telefone_cliente = serializers.CharField(max_length=20)
   
   def create(self, validated_data):
      agendamento = Agendamento.instanceects.create(
            data_horario=validated_data["data_horario"],
            nome_cliente=validated_data["nome_cliente"],
            email_cliente=validated_data["email_cliente"],
            telefone_cliente=validated_data["telefone_cliente"],
         )
      return agendamento
   
   def update(self, instance, validated_data):
      instance.data_horario = validated_data.get("data_horario", instance.data_horario)
      instance.nome_cliente = validated_data.get("nome_cliente", instance.nome_cliente)
      instance.email_cliente = validated_data.get("email_cliente", instance.email_cliente)
      instance.telefone_cliente = validated_data.get("telefone_cliente", instance.telefone_cliente)
      instance.save()
      return instance