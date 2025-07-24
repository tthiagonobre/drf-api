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