#  Agenda API  

API desenvolvida em **Django Rest Framework** para gerenciar agendamentos entre clientes e prestadores de serviço.  

Inclui validações de:  
-  Não permitir agendamentos no passado  
-  Bloqueio de agendamentos em feriados (via integração com [BrasilAPI](https://brasilapi.com.br/))  
-  Restrições de horários disponíveis  
-  Regras de consistência entre telefone e email  

---

##  Tecnologias  
- [Python 3.11+](https://www.python.org/)  
- [Django 5+](https://www.djangoproject.com/)  
- [Django REST Framework](https://www.django-rest-framework.org/)  

---

##  Instalação  

Clone o repositório:  
```bash
git clone https://github.com/seu-usuario/agenda-api.git
cd agenda-api
```

Crie e ative um ambiente virtual:  
```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

Instale as dependências:  
```bash
pip install -r requirements.txt
```

Execute as migrações e rode o servidor:  
```bash
python manage.py migrate
python manage.py runserver
```

A API estará disponível em:  
 `http://127.0.0.1:8000/`  

---

##  Endpoints principais  

###  Prestadores  
- `GET /prestadores/` → Lista todos os prestadores e seus agendamentos  
- `GET /prestadores/{id}/` → Detalhes de um prestador específico  

###  Agendamentos  
- `GET /agendamentos/` → Lista todos os agendamentos  
- `POST /agendamentos/` → Cria um novo agendamento  

Exemplo de corpo para `POST /agendamentos/`:  
```json
{
  "prestador": "joao123",
  "data_horario": "2025-08-25T14:00:00Z",
  "nome_cliente": "Thiago Nobre",
  "email_cliente": "thiago@email.com",
  "telefone_cliente": "+5511999999999"
}
```

- `GET /agendamentos/{id}/` → Detalhes de um agendamento  
- `DELETE /agendamentos/{id}/` → Cancela um agendamento  

---

##  Regras de validação  
- Não é possível agendar no passado.  
- Não é possível agendar em feriados nacionais (via BrasilAPI).  
- Apenas horários disponíveis podem ser utilizados (definidos em `utils.get_horarios_disponiveis`).  
- Emails terminados em `.br` devem estar associados a telefone do Brasil (`+55`).  

---

##  Futuras melhorias  
- Autenticação JWT para prestadores  
- Integração com agenda do Google Calendar  
- Notificações por email ou WhatsApp  

---

##  Licença  
Este projeto está sob a licença MIT.  
