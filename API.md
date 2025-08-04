#API


-Listar horários: GET /horarios/
["7:00", "19:30"]

-Listar agendamentos: GET /agendamentos/
[
   {
      "nome": "Thiago",
      "telefone": "6546454",
      "email": "thiago@gmail.com"
   }
]

-Criar agendamento: POST /agendamentos/

-Detalhar agendamento: GET /agendamentos/<id>/

-Deletar agendamento: DELETE /agendamentos/<id>

-Editar agendamento: PUT/PATCH /agendamentos/<id>


"""
- Qualquer cliente (autenticado ou não) seja capaz de criar um agendamento.
- Apenas o prestador de serviço pode vizualizar todos os agendamentos em sua agenda.
- Apenas o prestador de serviço pode manipular os seus agendamentos.
"""