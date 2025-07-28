from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from agenda.serializers import AgendamentoSerializer
from agenda.models import Agendamento

# Create your views here.
@api_view(http_method_names=["GET", "PATCH", "DELETE"])
def agendamento_detail(request, id):
   obj = get_object_or_404(Agendamento, id=id)
   if request.method == "GET":
      serializer = AgendamentoSerializer(obj)
      return JsonResponse(serializer.data)
   if request.method == "PATCH":
      data = request.data
      serializer = AgendamentoSerializer(obj, data=data, partial=True)
      if serializer.is_valid():
         serializer.save()
         return JsonResponse(serializer.data, status=200)
      return JsonResponse(serializer.errors, status=400)
   if request.method == "DELETE":
      obj.cancelado = True
      obj.save()
      return Response(status=204)
      

@api_view(http_method_names=["GET", "POST"])
def agendamento_list(request):
   if request.method == "GET":
      cancelado = request.GET.get("cancelado")  # ?cancelado=true ou false
      if cancelado is not None:
         # Converte o valor da query string para booleano
         if cancelado.lower() == "true":
            qs = Agendamento.objects.filter(cancelado=True)
         elif cancelado.lower() == "false":
            qs = Agendamento.objects.filter(cancelado=False)
         else:
            # Valor inválido (nem "true" nem "false")
            return JsonResponse({"erro": "Valor inválido para 'cancelado'. Use true ou false."}, status=400)
      else:
         # Se não passar nenhum parâmetro, retorna todos
         qs = Agendamento.objects.all()

      serializer = AgendamentoSerializer(qs, many=True)
      return JsonResponse(serializer.data, safe=False)

   if request.method == "POST":
      data = request.data
      serializer = AgendamentoSerializer(data=data)
      if serializer.is_valid():
         serializer.save()
         return JsonResponse(serializer.data, status=201)
      return JsonResponse(serializer.errors, status=400)