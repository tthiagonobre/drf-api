from datetime import datetime
from rest_framework.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, generics
from rest_framework import permissions
from django.contrib.auth.models import User
from agenda.serializers import AgendamentoSerializer, PrestadorSerializer
from agenda.models import Agendamento
from agenda.utils import get_horarios_disponiveis


# Create your views here.
class IsOwnerOrCreateOnly(permissions.BasePermission):
   def has_permission(self, request, view):
      # Para criar (POST) qualquer um pode (mesmo não autenticado)
      if request.method == "POST":
         return True

      # Bloqueia quem não está logado
      if not request.user.is_authenticated:
         return False

      # Só o dono pode acessar os dados dele
      username = request.query_params.get("username")
      if request.user.username == username:
         return True

      return False


   
class IsPrestador(permissions.BasePermission):
   def has_object_permission(self, request, view, obj):
      if obj.prestador == request.user:
         return True
      return False
      

class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):
   permission_classes = [IsPrestador]
   queryset = Agendamento.objects.all()
   serializer_class = AgendamentoSerializer
   
   def delete(self, request, *args, **kwargs):
      obj = self.get_object()
      obj.cancelado = True
      obj.save()
      return Response(status=204)
  

class AgendamentoList(generics.ListCreateAPIView):
   permission_classes = [IsOwnerOrCreateOnly]
   serializer_class = AgendamentoSerializer
   
   def get_queryset(self):
      username = self.request.query_params.get("username")
      if not username:
         return Agendamento.objects.none()
      
      queryset = Agendamento.objects.filter(prestador__username=username)
      
      cancelado = self.request.query_params.get("cancelado")
      if cancelado is None:
         return queryset
      
      if cancelado.lower() == "true":
         return queryset.filter(cancelado=True)
      elif cancelado.lower() == "false":
         return queryset.filter(cancelado=False)
      
      raise ValidationError({"error": "Valor inválido (use true ou false)."})
   
   
class PrestadorList(generics.ListAPIView):
   permission_classes = [permissions.IsAdminUser]  # Apenas superuser pode acessar
   serializer_class = PrestadorSerializer
   queryset = User.objects.all()
   

@api_view(http_method_names=["GET"])
def get_horario(request):
   data = request.query_params.get("data")
   if not data:
      data = datetime.now().date()
   else:
      data = datetime.fromisoformat(data).date()
   
   horarios_disponiveis = sorted(list(get_horarios_disponiveis(data)))
   return JsonResponse(horarios_disponiveis, safe=False)
