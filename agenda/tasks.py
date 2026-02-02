import csv
from io import StringIO

from django.contrib.auth.models import User

from agenda.serializers import PrestadorSerializer
from tamarcado.celery import app

from django.core.mail import EmailMessage


def gera_relatorio():
   output = StringIO()
   writer = csv.writer(output)
   writer.writerow([
      "prestador",
      "data_horario",
      "nome_cliente",
      "email_cliente",
      "telefone_cliente",
      "cancelado",
   ])
   
   prestadores = User.objects.all().prefetch_related('agendamentos')
   serializer = PrestadorSerializer(prestadores, many=True)
   for prestador in serializer.data:
      for agendamento in prestador["agendamentos"]:
               writer.writerow([
                  agendamento["prestador"],
                  agendamento["data_horario"],
                  agendamento["nome_cliente"],
                  agendamento["email_cliente"],
                  agendamento["telefone_cliente"],
                  agendamento["cancelado"],
               ])
   
   conteudo = output.getvalue()
   output.close()
   return conteudo
   
   
def envia_email_com_anexo(conteudo_csv, destinatario):
   email = EmailMessage(
      'tamarcado - Relatório de prestadores',
      'Em anexo o relatório solicitado.',
      'tcardosonobre@gmail.com',
      [destinatario],
   )            
   email.attach("relatorio.csv", conteudo_csv, "text/csv")
   email.send()


@app.task
def gera_relatorio_prestadores(destinatario="thiagocardoso.nobre@gmail.com"):
   csv_data = gera_relatorio()
   envia_email_com_anexo(csv_data, destinatario)