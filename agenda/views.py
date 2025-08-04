from rest_framework.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, generics

from agenda.serializers import AgendamentoSerializer
from agenda.models import Agendamento

# Create your views here.
class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):
   queryset = Agendamento.objects.all()
   serializer_class = AgendamentoSerializer
   
   def delete(self, request, *args, **kwargs):
      obj = self.get_object()
      obj.cancelado = True
      obj.save()
      return Response(status=204)
  

class AgendamentoList(generics.ListCreateAPIView):
   queryset = Agendamento.objects.all()
   serializer_class = AgendamentoSerializer
   
   def get_queryset(self):
      cancelado = self.request.GET.get("cancelado")  # ?cancelado=true ou false
      if cancelado is None:
         return Agendamento.objects.all() 

      if cancelado.lower() == "true":
         return Agendamento.objects.filter(cancelado=True)
      elif cancelado.lower() == "false":
         return Agendamento.objects.filter(cancelado=False)
      
      raise ValidationError({"error": "Valor inválido (use 'true' ou 'false')."})
   

@api_view(http_method_names=["GET"])
def get_horario(request):
   data = request.query_params.get("data")
   if not data:
      data = datetime.now().date()
   else:
      data = datetime.fromisoformat(data).date()
      
   horarios_disponiveis = sorted(list(get_horarios_disponiveis(data)))
   return JsonResponse(horarios_disponiveis, safe=False)